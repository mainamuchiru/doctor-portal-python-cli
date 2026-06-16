from utils.utils import prompt, divider, header
from menu.patient_menu import create_patient, view_patient_history, update_patient
from menu.doctor_menu import update_doctor_details
from menu.session_menu import diagnose_patient


def main_menu(doctor):
    while True:
        header(f"Main Menu  --  Dr. {doctor.name}")
        print("  1. Diagnose Patient")
        print("  2. Create Patient")
        print("  3. View Patient History")
        print("  4. Update Patient Details")
        print("  5. Update My Details")
        print("  6. Logout")
        divider()
        choice = prompt("Choose an option: ")

        if choice == "1":
            diagnose_patient(doctor)
        elif choice == "2":
            create_patient(doctor)
        elif choice == "3":
            view_patient_history()
        elif choice == "4":
            update_patient(doctor)
        elif choice == "5":
            update_doctor_details(doctor)
        elif choice == "6":
            print(f"\n[OK] Logged out. Goodbye, Dr. {doctor.name}!\n")
            break
        else:
            print("[!] Please enter a number between 1 and 6.")
