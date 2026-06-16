import Diagnosis.storage
from Diagnosis.doctor import Doctor
from utils.utils import prompt, divider, header


def auth_menu():
    while True:
        header("Doctor Portal")
        print("  1. Login")
        print("  2. Sign Up")
        print("  3. Exit")
        divider()
        choice = prompt("Choose an option: ")

        if choice == "1":
            doctor = login()
            if doctor:
                from menu.main_menu import main_menu
                main_menu(doctor)
        elif choice == "2":
            sign_up()
        elif choice == "3":
            print("\nGoodbye!\n")
            break
        else:
            print("[!] Please enter 1, 2, or 3.")


def login():
    header("Login")
    doctor_id = prompt("Doctor ID: ")
    password = prompt("Password : ")

    doctor: Doctor = Diagnosis.storage.login_doctor(doctor_id, password)
    if not doctor or not doctor.check_password(password):
        print("[!] Invalid Doctor ID or password. Please try again.")
        return None

    print(f"\n[OK] Welcome back, Dr. {doctor.name}!")
    return doctor


def sign_up():
    header("Create Doctor Account")
    name = prompt("Full Name  : ")
    doctor_id = prompt("Doctor ID  : ")
    password = prompt("Password   : ")

    if not name or not doctor_id or not password:
        print("[!] All fields are required.")
        return

    new_doctor = Doctor(name, doctor_id, password)

    try:
        saved = Diagnosis.storage.register_doctor(new_doctor.name, new_doctor.doctor_id, new_doctor.password)
    except ValueError as e:
        print(f"[!] {e}")
        return

    if not saved:
        print("[!] That Doctor ID is already taken. Please try a different one.")
    else:
        print(f"\n[OK] Account created. Welcome, Dr. {saved.name}!")
