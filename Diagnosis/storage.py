import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from Diagnosis.doctor import Doctor
from Diagnosis.patient import Patient

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = BASE_DIR / "json"

DOCTORS_FILE = JSON_DIR / "doctors.json"
PATIENTS_FILE = JSON_DIR / "patients.json"
DIAGNOSES_FILE = JSON_DIR / "diagnoses.json"
SESSIONS_FILE = JSON_DIR / "sessions.json"
DISEASES_FILE = JSON_DIR / "knowledge_base.json"


def load_json(filename: Path) -> Dict[str, Any]:
    try:
        if not filename.exists():
            return {}
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"{filename.name} contains invalid JSON.") from exc


def save_json(filename: Path, data: Dict[str, Any]) -> None:
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def register_doctor(name: str, doctor_id: str, password: str) -> Optional[Doctor]:
    doctor = Doctor(name, doctor_id, password)
    if not doctor.name or not doctor.doctor_id or not doctor.password:
        raise ValueError("Doctor name, ID, and password are required.")

    doctors = load_json(DOCTORS_FILE)
    if doctor.doctor_id in doctors:
        return None

    doctors[doctor.doctor_id] = doctor.to_dict()
    save_json(DOCTORS_FILE, doctors)
    return doctor


def login_doctor(doctor_id: str, password: str) -> Optional[Doctor]:
    doctors = load_json(DOCTORS_FILE)
    record = doctors.get(doctor_id)
    if not record:
        return None

    doctor = Doctor.from_dict(record)
    return doctor if doctor.check_password(password) else None


def update_doctor(doctor_id: str, new_name: str = "", new_password: str = "") -> bool:
    doctors = load_json(DOCTORS_FILE)
    if doctor_id not in doctors:
        return False

    doctor = Doctor.from_dict(doctors[doctor_id])
    doctor.update(new_name, new_password)
    doctors[doctor_id] = doctor.to_dict()
    save_json(DOCTORS_FILE, doctors)
    return True


def save_patient(patient: Patient) -> Patient:
    patient.validate()
    patients = load_json(PATIENTS_FILE)
    patients[patient.patient_id] = patient.to_dict()
    save_json(PATIENTS_FILE, patients)
    return patient


def get_all_patients() -> List[Patient]:
    patients = load_json(PATIENTS_FILE)
    return [Patient.from_dict(data) for data in patients.values()]


def get_patient_by_name(name: str) -> Optional[Patient]:
    patients = load_json(PATIENTS_FILE)
    name = name.strip().lower()

    for record in patients.values():
        if record.get("name", "").strip().lower() == name:
            return Patient.from_dict(record)

    return None


def get_patient_by_id(patient_id: str) -> Optional[Patient]:
    patients = load_json(PATIENTS_FILE)
    record = patients.get(patient_id)
    return Patient.from_dict(record) if record else None


def update_patient(
    patient_id: str,
    new_name: str = "",
    new_phone: str = "",
    new_dob: str = "",
    new_height: str = "",
    new_weight: str = "",
) -> bool:
    patients = load_json(PATIENTS_FILE)
    if patient_id not in patients:
        return False

    patient = Patient.from_dict(patients[patient_id])
    patient.update(new_name, new_phone, new_dob, new_height, new_weight)
    patient.validate()
    patients[patient_id] = patient.to_dict()
    save_json(PATIENTS_FILE, patients)
    return True


def search_patients_by_name(name: str) -> List[Patient]:
    needle = name.lower().strip()
    return [patient for patient in get_all_patients() if needle in patient.name.lower()]


def delete_patient(patient_id: str) -> bool:
    patients = load_json(PATIENTS_FILE)
    if patient_id not in patients:
        return False

    del patients[patient_id]
    save_json(PATIENTS_FILE, patients)

    diagnoses = load_json(DIAGNOSES_FILE)
    save_json(
        DIAGNOSES_FILE,
        {k: v for k, v in diagnoses.items() if v.get("patient_id") != patient_id},
    )

    sessions = load_json(SESSIONS_FILE)
    save_json(
        SESSIONS_FILE,
        {k: v for k, v in sessions.items() if v.get("patient_id") != patient_id},
    )

    return True


def save_diagnosis(diagnosis_dict: Dict[str, Any]) -> Dict[str, Any]:
    diagnoses = load_json(DIAGNOSES_FILE)
    diagnoses[diagnosis_dict["session_id"]] = diagnosis_dict
    save_json(DIAGNOSES_FILE, diagnoses)
    return diagnosis_dict


def get_patient_diagnoses(patient_id: str) -> List[Dict[str, Any]]:
    diagnoses = load_json(DIAGNOSES_FILE)
    return [d for d in diagnoses.values() if d.get("patient_id") == patient_id]


def save_session(session_dict: Dict[str, Any]) -> Dict[str, Any]:
    sessions = load_json(SESSIONS_FILE)
    sessions[session_dict["session_id"]] = session_dict
    save_json(SESSIONS_FILE, sessions)
    return session_dict


def get_patient_sessions(patient_id: str) -> List[Dict[str, Any]]:
    sessions = load_json(SESSIONS_FILE)
    return [s for s in sessions.values() if s.get("patient_id") == patient_id]


def search_diseases_by_symptom(symptom: str):
    if not DISEASES_FILE.exists():
        return []

    try:
        with DISEASES_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    symptoms_input = [s.strip().lower() for s in symptom.split(",")]

    diseases = data.get("diseases", [])
    matches = []

    for disease in diseases:
        if not isinstance(disease, dict):
            continue

        disease_symptoms = [s.lower() for s in disease.get("symptoms", [])]

        if any(s in disease_symptoms for s in symptoms_input):
            matches.append(disease)

    return matches