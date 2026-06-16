import argparse
import sys
from typing import Optional, List, Any

# Add the current directory to sys.path for modular imports
import getpass
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import storage
from models.patient import Patient
from models.diagnosis import Diagnosis
from models.session import Session
from utils.auth import log_action

try:
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
except ImportError:
    Console = None
    Table = None
    Prompt = None
    Confirm = None

console = Console() if Console else None

def write(message: str = "") -> None:
    if console:
        console.print(message)
    else:
        print(message)

LOGO = """
 ██████╗██╗     ██╗███╗   ██╗██╗ ██████╗ 
██╔════╝██║     ██║████╗  ██║██║██╔════╝ 
██║     ██║     ██║██╔██╗ ██║██║██║      
██║     ██║     ██║██║╚██╗██║██║██║      
╚██████╗███████╗██║██║ ╚████║██║╚██████╗ 
 ╚═════╝╚══════╝╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ 
        MEDICAL PORTAL SYSTEM
"""

def print_logo():
    if console:
        console.print(f"[bold cyan]{LOGO}[/bold cyan]")
    else:
        print(LOGO)

# --- Command Handlers ---

@log_action
def cmd_register_doctor(args) -> None:
    doctor = storage.register_doctor(args.name, args.doctor_id, args.password)
    if not doctor:
        write("[bold red]Error:[/bold red] A doctor with that ID already exists.")
        return
    write(f"Doctor account created for Dr. {doctor.name} ({doctor.user_id}).")

@log_action
def cmd_login(args) -> None:
    user = storage.login_user(args.doctor_id, args.password)
    if not user:
        write("[bold red]Error:[/bold red] Invalid ID or password.")
        return
    write(f"Login successful. Welcome {user.name} ({user.role}).")
    return user

@log_action
def cmd_add_patient(args) -> None:
    patient = Patient(args.name, args.phone, args.dob, args.height or "", args.weight or "")
    patient.save()
    write(f"Patient [bold green]{patient.name}[/bold green] added with ID: {patient.patient_id}")

@log_action
def cmd_list_patients(args=None) -> None:
    patients = Patient.get_all()
    if not patients:
        write("No patients found.")
        return
    
    if console and Table:
        table = Table(title="Patient Records")
        for col in ["ID", "Name", "Phone", "DOB", "Height", "Weight"]:
            table.add_column(col)
        for p in patients:
            table.add_row(p.patient_id, p.name, p.phone_number, p.date_of_birth, p.height or "-", p.weight or "-")
        console.print(table)
    else:
        write("ID | Name | Phone | DOB | H | W")
        for p in patients:
            write(f"{p.patient_id} | {p.name} | {p.phone_number} | {p.date_of_birth} | {p.height} | {p.weight}")

@log_action
def cmd_match_diagnosis(args) -> None:
    matches = Diagnosis.match_symptoms(args.symptoms)
    if not matches:
        write("No matching diseases found.")
        return
    
    if console and Table:
        table = Table(title="Possible Diagnoses")
        table.add_column("Disease", style="cyan")
        table.add_column("Score", justify="center")
        table.add_column("Matched Symptoms")
        table.add_column("Medication", style="green")
        for m in matches:
            table.add_row(m["name"], str(m["score"]), ", ".join(m["matched_symptoms"]), m["medication"])
        console.print(table)
    else:
        for m in matches:
            write(f"{m['name']} (Score: {m['score']}): {', '.join(m['matched_symptoms'])}")

# --- Interactive Mode ---

def prompt_input(prompt_text: str, password: bool = False) -> str:
    """Read input from the terminal."""
    return input(f"{prompt_text}: ")


def interactive_menu():
    user = None
    while True:
        if not user:
            write("\n1. Register Doctor\n2. Login\n3. Exit")
            choice = input("Choose an option (1/2/3): ").strip()

            if choice == "1":
                name = prompt_input("Name")
                doc_id = prompt_input("Doctor ID")
                pw = prompt_input("Password", password=True)
                cmd_register_doctor(argparse.Namespace(name=name, doctor_id=doc_id, password=pw))
            elif choice == "2":
                doc_id = prompt_input("Doctor ID")
                pw = prompt_input("Password", password=True)
                user = storage.login_user(doc_id, pw)
                if user:
                    write(f"Welcome Dr. {user.name}!")
                else:
                    write("Login failed.")
            elif choice == "3":
                break
            else:
                write("Please enter 1, 2 or 3.")
        else:
            write(f"\nMain Menu (Dr. {user.name})")
            write("1. Add Patient\n2. List Patients\n3. Match Diagnosis\n4. Logout\n5. Exit")
            choice = input("Choose an option (1-5): ").strip()

            if choice == "1":
                name = prompt_input("Patient Name")
                phone = prompt_input("Phone")
                dob = prompt_input("DOB (YYYY-MM-DD)")
                h = prompt_input("Height (optional)")
                w = prompt_input("Weight (optional)")
                cmd_add_patient(argparse.Namespace(name=name, phone=phone, dob=dob, height=h, weight=w))
            elif choice == "2":
                cmd_list_patients()
            elif choice == "3":
                syms = prompt_input("Enter symptoms (comma separated)").split(",")
                cmd_match_diagnosis(argparse.Namespace(symptoms=[s.strip() for s in syms]))
            elif choice == "4":
                user = None
                write("Logged out.")
            elif choice == "5":
                break
            else:
                write("Please enter a valid option between 1 and 5.")

# --- Parser Setup ---

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Medical Portal - Modular CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Registration
    reg = subparsers.add_parser("register", help="Register a new doctor")
    reg.add_argument("--name", required=True)
    reg.add_argument("--doctor-id", required=True)
    reg.add_argument("--password", required=True)
    reg.set_defaults(func=cmd_register_doctor)

    # Login
    login = subparsers.add_parser("login", help="Login")
    login.add_argument("--doctor-id", required=True)
    login.add_argument("--password", required=True)
    login.set_defaults(func=cmd_login)

    # Add Patient
    add_p = subparsers.add_parser("add-patient", help="Add a new patient")
    add_p.add_argument("--name", required=True)
    add_p.add_argument("--phone", required=True)
    add_p.add_argument("--dob", required=True)
    add_p.add_argument("--height")
    add_p.add_argument("--weight")
    add_p.set_defaults(func=cmd_add_patient)

    # List Patients
    subparsers.add_parser("list-patients", help="List all patients").set_defaults(func=cmd_list_patients)

    # Diagnosis
    diag = subparsers.add_parser("diagnose", help="Match symptoms to diagnosis")
    diag.add_argument("symptoms", nargs="+")
    diag.set_defaults(func=cmd_match_diagnosis)

    # Interactive
    subparsers.add_parser("interactive", help="Start interactive menu").set_defaults(func=lambda x: interactive_menu())

    return parser

def main():
    print_logo()
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            if console:
                console.print_exception()
            else:
                write(f"An error occurred: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
