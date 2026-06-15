import functools
import getpass
import json
import sys
from datetime import datetime

from patient import Patient, PatientDeleter
from storage import StorageEngine


def require_doctor_privileges(func):
    @functools.wraps(func)
    def wrapper(instance, *args, **kwargs):
        role = getattr(instance, "role", None)
        if not role or role.lower() != "admin":
            raise PermissionError("Access Denied: Doctor privileges required.")
        return func(instance, *args, **kwargs)
    return wrapper


class User:
    def __init__(self, username, user_id, password, role):
        self._username = username
        self._user_id = user_id
        self._password = password
        self._role = role

    @property
    def username(self):
        return self._username

    @property
    def user_id(self):
        return self._user_id

    @property
    def role(self):
        return self._role

    def check_password(self, password_input):
        return self._password == password_input


class Doctor(User):
    def __init__(self, name, doctor_id, password):
        super().__init__(username=name, user_id=doctor_id, password=password, role="Admin")

    @property
    def name(self):
        return self.username

    @property
    def doctor_id(self):
        return self.user_id

    @require_doctor_privileges
    def view_patient_history(self, patient_id):
        return Patient.fetch_patient_history(patient_id)

    @require_doctor_privileges
    def create_patient(self, name, patient_id, date_of_birth, phone_number, height=None, weight=None):
        patient = Patient(name, patient_id, date_of_birth, phone_number, height, weight)
        return patient.add_new_patient()

    @require_doctor_privileges
    def diagnose_patient(self, session_id, patient_id, symptoms, disease, prevention, medication, storage_engine):
        diagnosis_data = {
            "session_id": session_id,
            "patient_id": patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": symptoms,
            "disease": disease,
            "prevention": prevention,
            "medication": medication,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        saved = storage_engine.save_diagnosis(diagnosis_data)
        if not saved:
            raise IOError("Failed to save diagnosis record.")
        return diagnosis_data

    @require_doctor_privileges
    def update_patient(self, patient_id, updated_fields):
        Patient._ensure_file_exists()

        try:
            with open(Patient.FILE_PATH, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}

        patient_data = data.get(patient_id)
        if not patient_data:
            raise ValueError(f"Patient with ID {patient_id} not found.")

        allowed_fields = ["name", "date_of_birth", "height", "weight", "phone_number"]
        for field, value in updated_fields.items():
            if field in allowed_fields:
                patient_data[field] = value

        data[patient_id] = patient_data
        with open(Patient.FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)

        return True

    @require_doctor_privileges
    def delete_patient(self, patient_id):
        return PatientDeleter.delete_patient(patient_id)


def authenticate_doctor(doctors, doctor_id, password):
    for doctor in doctors:
        if doctor.doctor_id == doctor_id and doctor.check_password(password):
            return doctor
    return None


def doctor_login_form(doctors):
    print("=" * 45)
    print("       CLINIC MANAGEMENT SYSTEM LOGIN        ")
    print("=" * 45)

    attempts = 3
    while attempts > 0:
        print(f"\n[Remaining Login Attempts: {attempts}]")
        doc_id = input("Enter Doctor ID: ").strip()
        password = getpass.getpass("Enter Secret Password: ")

        doctor_session = authenticate_doctor(doctors, doc_id, password)
        if doctor_session:
            print(f"\n[+] Access Granted. Welcome, Dr. {doctor_session.name}!")
            return doctor_session

        print("[!] Invalid Doctor ID or password.")
        attempts -= 1

    print("\n[!!!] Maximum authentication attempts reached. Exiting program.")
    sys.exit(1)


def display_doctor_menu():
    print("\nDoctor Menu")
    print("1. View Patient History")
    print("2. Create Patient")
    print("3. Update Patient")
    print("4. Delete Patient")
    print("5. Diagnose Patient")
    print("6. List All Patients")
    print("7. Quit")


def choose_disease(storage_engine):
    symptom = input("Enter patient symptom for search: ").strip()
    matches = storage_engine.search_diseases_by_symptom(symptom)
    if not matches:
        print("[!] No matching diseases found.")
        return None

    for idx, disease in enumerate(matches, start=1):
        print(f"{idx}. {disease.get('name', 'Unknown')}")

    try:
        choice = int(input("Select the disease number: "))
    except ValueError:
        print("[!] Invalid choice.")
        return None

    if choice < 1 or choice > len(matches):
        print("[!] Selection out of range.")
        return None

    return matches[choice - 1]


def run_doctor_cli(doctor):
    storage_engine = StorageEngine()

    while True:
        display_doctor_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            patient_id = input("Patient ID: ").strip()
            result = doctor.view_patient_history(patient_id)
            if result:
                print(json.dumps(result, indent=2))

        elif choice == "2":
            name = input("Patient name: ").strip()
            patient_id = input("Patient ID: ").strip()
            dob = input("Date of birth (YYYY-MM-DD): ").strip()
            phone = input("Phone number: ").strip()
            height = input("Height (optional): ").strip() or None
            weight = input("Weight (optional): ").strip() or None
            doctor.create_patient(name, patient_id, dob, phone, height, weight)

        elif choice == "3":
            patient_id = input("Patient ID to update: ").strip()
            updates = {}
            for field in ["name", "date_of_birth", "phone_number", "height", "weight"]:
                value = input(f"New {field} (leave blank to keep current): ").strip()
                if value:
                    updates[field] = value
            if updates:
                doctor.update_patient(patient_id, updates)
                print("[+] Patient updated successfully.")
            else:
                print("[!] No updates provided.")

        elif choice == "4":
            patient_id = input("Patient ID to delete: ").strip()
            if doctor.delete_patient(patient_id):
                print("[+] Patient deleted successfully.")

        elif choice == "5":
            patient_id = input("Patient ID: ").strip()
            session_id = input("Session ID: ").strip() or None
            disease_record = choose_disease(storage_engine)
            if disease_record is None:
                continue
            patient_symptoms = input("Enter symptom notes: ").strip()
            prevention = disease_record.get("prevention", "N/A")
            medication = disease_record.get("medication", "N/A")
            if not session_id:
                session_id = f"S-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            doctor.diagnose_patient(
                session_id=session_id,
                patient_id=patient_id,
                symptoms=patient_symptoms,
                disease=disease_record.get("name", "Unknown"),
                prevention=prevention,
                medication=medication,
                storage_engine=storage_engine,
            )
            print("[+] Diagnosis saved.")

        elif choice == "6":
            print(json.dumps(Patient.list_all_patients(), indent=2))

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("[!] Invalid selection. Please choose a valid menu item.")


if __name__ == "__main__":
    doctors = [
        Doctor("Alice Mwenda", "D101", "docpass"),
        Doctor("Brian Karanja", "D202", "secure123"),
    ]

    doctor = doctor_login_form(doctors)
    run_doctor_cli(doctor)
