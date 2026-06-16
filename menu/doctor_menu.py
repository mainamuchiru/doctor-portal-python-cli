import Diagnosis.storage
from utils.utils import prompt, header


def update_doctor_details(doctor):
    header("Update My Details")
    print(f"Editing: Dr. {doctor.name}  (leave blank to keep current value)\n")

    new_name     = prompt(f"  Name [{doctor.name}]: ")
    new_password = prompt("  New Password (leave blank to keep current): ")

    confirm  = prompt("\nConfirm current password to save changes: ")
    verified = Diagnosis.storage.login_doctor(doctor.doctor_id, confirm)
    if not verified:
        print("[!] Incorrect password. No changes were saved.")
        return

    Diagnosis.storage.update_doctor(doctor.doctor_id, new_name, new_password)

    if new_name:
        doctor.name = new_name.strip()

    print("[OK] Your details have been updated.")
