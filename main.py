import argparse
import sys
from typing import Optional, List

# Add the current directory to sys.path for modular imports
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
except ImportError:
    Console = None
    Table = None

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

@log_action
def cmd_register_doctor(args) -> None:
    doctor = storage.register_doctor(args.name, args.doctor_id, args.password)
    if not doctor:
        write("Error: A doctor with that ID already exists.")
        return
    write(f"Doctor account created for Dr. {doctor.name} ({doctor.user_id}).")

@log_action
def cmd_login(args) -> None:
    user = storage.login_user(args.doctor_id, args.password)
    if not user:
        write("Error: Invalid ID or password.")
        return
    write(f"Login successful. Welcome {user.name} ({user.role}).")

@log_action
def cmd_list_patients(args) -> None:
    patients = Patient.get_all()
    if not patients:
        write("No patients found.")
        return
    
    rows = [
        [p.patient_id, p.name, p.phone_number, p.date_of_birth, p.height or "-", p.weight or "-"]
        for p in patients
    ]
    
    if console and Table:
        table = Table(title="Patient Records")
        for col in ["ID", "Name", "Phone", "DOB", "Height", "Weight"]:
            table.add_column(col)
        for row in rows:
            table.add_row(*[str(val) for val in row])
        console.print(table)
    else:
        write("ID | Name | Phone | DOB | H | W")
        for row in rows:
            write(" | ".join(str(val) for val in row))

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Medical Portal - Modular CLI")
    subparsers = parser.add_subparsers(dest="command")

    reg = subparsers.add_parser("register-doctor", help="Register a new doctor")
    reg.add_argument("--name", required=True)
    reg.add_argument("--doctor-id", required=True)
    reg.add_argument("--password", required=True)
    reg.set_defaults(func=cmd_register_doctor)

    login = subparsers.add_parser("login", help="Login to the system")
    login.add_argument("--doctor-id", required=True)
    login.add_argument("--password", required=True)
    login.set_defaults(func=cmd_login)

    list_p = subparsers.add_parser("list-patients", help="List all patients")
    list_p.set_defaults(func=cmd_list_patients)

    return parser

def main():
    print_logo()
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        try:
            args.func(args)
        except Exception as e:
            write(f"[bold red]Error:[/bold red] {str(e)}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
