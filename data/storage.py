import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from models.doctor import Doctor, Admin
from models.patient import Patient

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "json_data"
DATA_DIR.mkdir(exist_ok=True)

DOCTORS_FILE = DATA_DIR / "doctors.json"
PATIENTS_FILE = DATA_DIR / "patients.json"
DIAGNOSES_FILE = DATA_DIR / "diagnoses.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"

def load_json(filename: Path) -> Dict[str, Any]:
    try:
        if not filename.exists():
            return {}
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}

def save_json(filename: Path, data: Dict[str, Any]) -> None:
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def register_doctor(name: str, doctor_id: str, password_raw: str) -> Optional[Doctor]:
    from utils.auth import hash_password
    doctors = load_json(DOCTORS_FILE)
    if doctor_id in doctors:
        return None
    
    doctor = Doctor(name, doctor_id, hash_password(password_raw))
    doctors[doctor_id] = doctor.to_dict()
    save_json(DOCTORS_FILE, doctors)
    return doctor

def login_user(user_id: str, password_raw: str) -> Optional[Any]:
    from utils.auth import hash_password
    doctors = load_json(DOCTORS_FILE)
    record = doctors.get(user_id)
    if not record:
        return None
    
    # Simple role detection for login
    if record.get("role") == "admin":
        user = Admin.from_dict(record)
    else:
        user = Doctor.from_dict(record)
        
    if user.check_password(password_raw):
        return user
    return None

def save_patient(patient: Patient) -> Patient:
    patient.validate()
    patients = load_json(PATIENTS_FILE)
    patients[patient.patient_id] = patient.to_dict()
    save_json(PATIENTS_FILE, patients)
    return patient

def get_all_patients() -> List[Patient]:
    patients = load_json(PATIENTS_FILE)
    return [Patient.from_dict(data) for data in patients.values()]

def get_patient_by_id(patient_id: str) -> Optional[Patient]:
    patients = load_json(PATIENTS_FILE)
    record = patients.get(patient_id)
    return Patient.from_dict(record) if record else None

def delete_patient(patient_id: str) -> bool:
    patients = load_json(PATIENTS_FILE)
    if patient_id not in patients:
        return False
    del patients[patient_id]
    save_json(PATIENTS_FILE, patients)
    return True

# ... Add other storage methods as needed ...
