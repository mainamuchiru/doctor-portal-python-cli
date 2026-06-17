import sys
import json
from pathlib import Path
import getpass
import Diagnosis.storage as storage
from Diagnosis.session import Session
from Diagnosis.diagnosis import Diagnosis
from utils.utils import prompt

SESSION_FILE = Path(__file__).resolve().parent / "json" / "session_state.json"


def save_login(doctor):
    data = {
        "doctor_id": doctor.doctor_id,
        "name": doctor.name
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)


def load_login():
    if not SESSION_FILE.exists():
        return None

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def logout():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()
    print("[OK] Logged out")


def login():
    doctor_id = prompt("Doctor ID: ")
    password = getpass.getpass("Password: ") 

    doctor = storage.login_doctor(doctor_id, password)

    if not doctor:
        print("[!] Invalid login")
        return None

    save_login(doctor)
    print(f"[OK] Welcome Dr. {doctor.name}")
    return doctor


def require_login():
    data = load_login()

    if not data:
        print("[!] Please login first using: python main.py login")
        return None

    return data


def add_patient():
    doctor = require_login()
    if not doctor:
        return

    from Diagnosis.patient import Patient

    name = prompt("Name: ")
    phone = prompt("Phone: ")
    dob = prompt("Date of Birth: ")

    patient = Patient(name, phone, dob)
    storage.save_patient(patient)

    print("[OK] Patient added")


def list_patients():
    doctor = require_login()
    if not doctor:
        return

    patients = storage.get_all_patients()

    if not patients:
        print("[!] No patients found")
        return

    for p in patients:
        print(p)


def diagnose():
    doctor = require_login()
    if not doctor:
        return

    from utils.utils import header
    header("Diagnose Patient")

    name = prompt("Patient Name: ")
    patient = storage.get_patient_by_name(name)

    if not patient:
        print("[!] Patient not found")
        return

    session = Session(patient.patient_id, doctor["doctor_id"])
    session.start_time()

    diag = Diagnosis(session.session_id, patient.patient_id, doctor["doctor_id"])

    if not diag.enter_symptoms(storage):
        session.update_status("cancelled")
        storage.save_session(session.to_dict())
        print("[!] Diagnosis cancelled")
        return

    diag.show_summary()

    notes = prompt("Notes: ")
    if notes:
        session.record_notes(notes)

    session.end_time()
    session.diagnosis = diag.disease

    storage.save_diagnosis(diag.to_dict())
    storage.save_session(session.to_dict())

    print("[OK] Diagnosis complete")


def delete_patient():
    doctor = require_login()
    if not doctor:
        return

    patient_id = prompt("Patient ID: ")

    if storage.delete_patient(patient_id):
        print("[OK] Patient deleted")
    else:
        print("[!] Patient not found")


def main():
    if len(sys.argv) < 2:
        print("Commands: login | logout | add-patient | list-patients | diagnose | delete-patient")
        return

    command = sys.argv[1]

    if command == "login":
        login()

    elif command == "logout":
        logout()

    elif command == "add-patient":
        add_patient()

    elif command == "list-patients":
        list_patients()

    elif command == "diagnose":
        diagnose()

    elif command == "delete-patient":
        delete_patient()

    else:
        print("[!] Unknown command")


if __name__ == "__main__":
    main()