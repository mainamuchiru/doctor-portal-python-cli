import argparse
from typing import Iterable, List, Optional

import storage
from diagnosis import Diagnosis
from patient import Patient, PatientDeleter
from session import Session

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - fallback keeps the CLI usable without install
    Console = None
    Table = None

console = Console() if Console else None


def write(message: str = "") -> None:
    if console:
        console.print(message)
    else:
        print(message)


def render_rows(title: str, columns: List[str], rows: Iterable[Iterable[str]]) -> None:
    rows = list(rows)
    if console and Table:
        table = Table(title=title)
        for column in columns:
            table.add_column(column)
        for row in rows:
            table.add_row(*[str(value) for value in row])
        console.print(table)
        return

    write(title)
    write("-" * len(title))
    write(" | ".join(columns))
    for row in rows:
        write(" | ".join(str(value) for value in row))


def require_doctor(doctor_id: str, password: str):
    doctor = storage.login_doctor(doctor_id, password)
    if not doctor:
        raise ValueError("Invalid doctor ID or password.")
    return doctor


def cmd_register_doctor(args) -> None:
    doctor = storage.register_doctor(args.name, args.doctor_id, args.password)
    if not doctor:
        raise ValueError("A doctor with that ID already exists.")
    write(f"Doctor account created for Dr. {doctor.name} ({doctor.doctor_id}).")


def cmd_login(args) -> None:
    doctor = require_doctor(args.doctor_id, args.password)
    write(f"Login successful. Welcome Dr. {doctor.name}.")


def cmd_update_doctor(args) -> None:
    require_doctor(args.doctor_id, args.current_password)
    updated = storage.update_doctor(args.doctor_id, args.name or "", args.password or "")
    if not updated:
        raise ValueError("Doctor not found.")
    write("Doctor details updated.")


def cmd_add_patient(args) -> None:
    require_doctor(args.doctor_id, args.password)
    patient = Patient(
        name=args.name,
        phone_number=args.phone,
        date_of_birth=args.dob,
        height=args.height or "",
        weight=args.weight or "",
    )
    storage.save_patient(patient)
    write(f"Patient created: {patient.name} ({patient.patient_id}).")


def cmd_list_patients(args) -> None:
    patients = storage.search_patients_by_name(args.search) if args.search else storage.get_all_patients()
    if not patients:
        write("No patients found.")
        return
    render_rows(
        "Patients",
        ["ID", "Name", "Phone", "DOB", "Height", "Weight"],
        [
            [
                patient.patient_id,
                patient.name,
                patient.phone_number,
                patient.date_of_birth,
                patient.height or "-",
                patient.weight or "-",
            ]
            for patient in patients
        ],
    )


def cmd_show_patient(args) -> None:
    patient = storage.get_patient_by_id(args.patient_id)
    if not patient:
        raise ValueError("Patient not found.")

    render_rows(
        "Patient Details",
        ["Field", "Value"],
        [
            ["ID", patient.patient_id],
            ["Name", patient.name],
            ["Phone", patient.phone_number],
            ["DOB", patient.date_of_birth],
            ["Height", patient.height or "-"],
            ["Weight", patient.weight or "-"],
        ],
    )

    sessions = storage.get_patient_sessions(patient.patient_id)
    diagnoses = storage.get_patient_diagnoses(patient.patient_id)
    write(f"Sessions: {len(sessions)}")
    write(f"Diagnoses: {len(diagnoses)}")


def cmd_update_patient(args) -> None:
    require_doctor(args.doctor_id, args.password)
    updated = storage.update_patient(
        args.patient_id,
        args.name or "",
        args.phone or "",
        args.dob or "",
        args.height or "",
        args.weight or "",
    )
    if not updated:
        raise ValueError("Patient not found.")
    write("Patient details updated.")


def cmd_delete_patient(args) -> None:
    require_doctor(args.doctor_id, args.password)
    if not PatientDeleter.delete_patient(args.patient_id):
        raise ValueError("Patient not found.")
    write("Patient and related history deleted.")


def cmd_match_diagnosis(args) -> None:
    matches = Diagnosis.match_symptoms(args.symptoms)
    if not matches:
        write("No matching diseases found.")
        return
    render_rows(
        "Possible Diagnoses",
        ["Disease", "Score", "Matched Symptoms", "Medication"],
        [
            [
                match["name"],
                str(match["score"]),
                ", ".join(match["matched_symptoms"]),
                match["medication"],
            ]
            for match in matches
        ],
    )


def cmd_record_session(args) -> None:
    doctor = require_doctor(args.doctor_id, args.password)
    patient = storage.get_patient_by_id(args.patient_id)
    if not patient:
        raise ValueError("Patient not found.")

    session = Session(patient.patient_id, doctor.doctor_id, args.diagnosis or "")
    session.start_session()
    if args.notes:
        session.add_notes(args.notes)
    session.end_session()
    storage.save_session(session.to_dict())
    write(f"Session saved for {patient.name}.")


def prompt(message: str) -> str:
    return input(message).strip()


def interactive() -> None:
    write("Doctor Portal Interactive Mode")
    while True:
        write("\n1. Register Doctor\n2. Login\n3. Exit")
        choice = prompt("Choose: ")
        if choice == "1":
            doctor = storage.register_doctor(prompt("Name: "), prompt("Doctor ID: "), prompt("Password: "))
            write("Account created." if doctor else "Doctor ID already exists.")
        elif choice == "2":
            doctor = storage.login_doctor(prompt("Doctor ID: "), prompt("Password: "))
            if doctor:
                interactive_menu(doctor)
            else:
                write("Invalid doctor ID or password.")
        elif choice == "3":
            return
        else:
            write("Choose 1, 2, or 3.")


def interactive_menu(doctor) -> None:
    while True:
        write(f"\nMain Menu - Dr. {doctor.name}")
        write("1. Add Patient\n2. List Patients\n3. Match Diagnosis\n4. Record Session\n5. Logout")
        choice = prompt("Choose: ")
        if choice == "1":
            patient = Patient(
                prompt("Patient Name: "),
                prompt("Phone Number: "),
                prompt("Date of Birth (YYYY-MM-DD): "),
                prompt("Height in cm (optional): "),
                prompt("Weight in kg (optional): "),
            )
            storage.save_patient(patient)
            write(f"Patient created: {patient.patient_id}")
        elif choice == "2":
            cmd_list_patients(argparse.Namespace(search=""))
        elif choice == "3":
            symptoms = prompt("Symptoms separated by commas: ").split(",")
            cmd_match_diagnosis(argparse.Namespace(symptoms=symptoms))
        elif choice == "4":
            patient_id = prompt("Patient ID: ")
            session = Session(patient_id, doctor.doctor_id, prompt("Diagnosis: "))
            session.start_session()
            session.add_notes(prompt("Notes: "))
            session.end_session()
            storage.save_session(session.to_dict())
            write("Session saved.")
        elif choice == "5":
            return
        else:
            write("Choose a number between 1 and 5.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Doctor Portal Python CLI")
    subparsers = parser.add_subparsers(dest="command")

    register = subparsers.add_parser("register-doctor", help="Create a doctor account")
    register.add_argument("--name", required=True)
    register.add_argument("--doctor-id", required=True)
    register.add_argument("--password", required=True)
    register.set_defaults(func=cmd_register_doctor)

    login = subparsers.add_parser("login", help="Check doctor credentials")
    login.add_argument("--doctor-id", required=True)
    login.add_argument("--password", required=True)
    login.set_defaults(func=cmd_login)

    update_doctor = subparsers.add_parser("update-doctor", help="Update doctor details")
    update_doctor.add_argument("--doctor-id", required=True)
    update_doctor.add_argument("--current-password", required=True)
    update_doctor.add_argument("--name")
    update_doctor.add_argument("--password")
    update_doctor.set_defaults(func=cmd_update_doctor)

    add_patient = subparsers.add_parser("add-patient", help="Create a patient record")
    add_patient.add_argument("--doctor-id", required=True)
    add_patient.add_argument("--password", required=True)
    add_patient.add_argument("--name", required=True)
    add_patient.add_argument("--phone", required=True)
    add_patient.add_argument("--dob", required=True)
    add_patient.add_argument("--height")
    add_patient.add_argument("--weight")
    add_patient.set_defaults(func=cmd_add_patient)

    list_patients = subparsers.add_parser("list-patients", help="List or search patients")
    list_patients.add_argument("--search", default="")
    list_patients.set_defaults(func=cmd_list_patients)

    show_patient = subparsers.add_parser("show-patient", help="Show patient details and counts")
    show_patient.add_argument("patient_id")
    show_patient.set_defaults(func=cmd_show_patient)

    update_patient = subparsers.add_parser("update-patient", help="Update a patient")
    update_patient.add_argument("patient_id")
    update_patient.add_argument("--doctor-id", required=True)
    update_patient.add_argument("--password", required=True)
    update_patient.add_argument("--name")
    update_patient.add_argument("--phone")
    update_patient.add_argument("--dob")
    update_patient.add_argument("--height")
    update_patient.add_argument("--weight")
    update_patient.set_defaults(func=cmd_update_patient)

    delete_patient = subparsers.add_parser("delete-patient", help="Delete a patient and related history")
    delete_patient.add_argument("patient_id")
    delete_patient.add_argument("--doctor-id", required=True)
    delete_patient.add_argument("--password", required=True)
    delete_patient.set_defaults(func=cmd_delete_patient)

    diagnosis = subparsers.add_parser("match-diagnosis", help="Rank possible diagnoses from symptoms")
    diagnosis.add_argument("symptoms", nargs="+")
    diagnosis.set_defaults(func=cmd_match_diagnosis)

    record_session = subparsers.add_parser("record-session", help="Record a completed consultation")
    record_session.add_argument("patient_id")
    record_session.add_argument("--doctor-id", required=True)
    record_session.add_argument("--password", required=True)
    record_session.add_argument("--diagnosis", default="")
    record_session.add_argument("--notes", default="")
    record_session.set_defaults(func=cmd_record_session)

    interactive_parser = subparsers.add_parser("interactive", help="Run the guided menu")
    interactive_parser.set_defaults(func=lambda args: interactive())
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    try:
        args.func(args)
        return 0
    except ValueError as exc:
        parser.exit(1, f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
