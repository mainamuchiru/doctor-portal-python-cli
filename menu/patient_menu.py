import Diagnosis.storage
from Diagnosis.patient import Patient
from utils.utils import prompt, divider, header


def create_patient(doctor):
    header("Create Patient")

    name   = prompt("Patient Name              : ")
    phone  = prompt("Phone Number              : ")
    dob    = prompt("Date of Birth (YYYY-MM-DD): ")
    height = prompt("Height in cm (optional)   : ")
    weight = prompt("Weight in kg (optional)   : ")

    try:
        patient = Patient(
            name=name,
            phone_number=phone,
            date_of_birth=dob,
            height=height,
            weight=weight,
        )
        patient.validate()
        Diagnosis.storage.save_patient(patient)
        print(f"\n[OK] Patient created successfully.")
        print(f"     Name      : {patient.name}")
        print(f"     Patient ID: {patient.patient_id}")
    except ValueError as e:
        print(f"[!] {e}")


def view_patient_history():
    header("Patient History")
    print("  1. View all patients")
    print("  2. Search patient by name")
    divider()
    choice = prompt("Choose: ")

    if choice == "1":
        patients = Diagnosis.storage.get_all_patients()
    elif choice == "2":
        name = prompt("Enter name to search: ")
        patients = Diagnosis.storage.search_patients_by_name(name)
    else:
        print("[!] Invalid option.")
        return

    if not patients:
        print("[!] No patients found.")
        return

    print(f"\n  {'ID':<38} {'Name':<20} {'DOB'}")
    divider()
    for p in patients:
        print(f"  {p.patient_id:<38} {p.name:<20} {p.date_of_birth}")

    divider()
    patient_id = prompt("Enter a Patient ID to view full history (or press Enter to go back): ")
    if not patient_id:
        return

    _show_patient_detail(patient_id)


def _show_patient_detail(patient_id):
    patient = Diagnosis.storage.get_patient_by_id(patient_id)
    if not patient:
        print("[!] Patient not found.")
        return

    header(f"Patient: {patient.name}")
    print(f"  ID    : {patient.patient_id}")
    print(f"  Phone : {patient.phone_number}")
    print(f"  DOB   : {patient.date_of_birth}")
    print(f"  Height: {patient.height or '-'}")
    print(f"  Weight: {patient.weight or '-'}")

    sessions  = Diagnosis.storage.get_patient_sessions(patient.patient_id)
    diagnoses = Diagnosis.storage.get_patient_diagnoses(patient.patient_id)

    print(f"\n  Total Sessions  : {len(sessions)}")
    print(f"  Total Diagnoses : {len(diagnoses)}")

    if sessions:
        print("\n  --- Sessions ---")
        for s in sessions:
            label = s.get("diagnosis") or "No diagnosis recorded"
            print(f"  [{s.get('status', '?').upper()}] {s.get('date_time', '')}  --  {label}")
            for note in s.get("notes", []):
                print(f"    Note ({note['timestamp']}): {note['note']}")

    if diagnoses:
        print("\n  --- Diagnoses ---")
        for d in diagnoses:
            print(f"  Disease   : {d.get('disease', '-')}")
            symptoms = d.get("symptoms", [])
            if isinstance(symptoms, list):
                print(f"  Symptoms  : {', '.join(symptoms)}")
            print(f"  Medication: {d.get('medication', '-')}")
            divider()


def update_patient(doctor):
    header("Update Patient Details")
    patient_id = prompt("Patient ID: ")

    patient = Diagnosis.storage.get_patient_by_id(patient_id)
    if not patient:
        print("[!] Patient not found.")
        return

    print(f"\nEditing: {patient.name}  (leave blank to keep current value)")
    name   = prompt(f"  Name [{patient.name}]: ")
    phone  = prompt(f"  Phone [{patient.phone_number}]: ")
    dob    = prompt(f"  Date of Birth [{patient.date_of_birth}]: ")
    height = prompt(f"  Height [{patient.height or '-'}]: ")
    weight = prompt(f"  Weight [{patient.weight or '-'}]: ")

    try:
        Diagnosis.storage.update_patient(patient_id, name, phone, dob, height, weight)
        print("[OK] Patient details updated successfully.")
    except ValueError as e:
        print(f"[!] {e}")
