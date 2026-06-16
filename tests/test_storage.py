from pathlib import Path

import pytest

import storage
from patient import Patient


@pytest.fixture()
def isolated_store(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DOCTORS_FILE", tmp_path / "doctors.json")
    monkeypatch.setattr(storage, "PATIENTS_FILE", tmp_path / "patients.json")
    monkeypatch.setattr(storage, "DIAGNOSES_FILE", tmp_path / "diagnoses.json")
    monkeypatch.setattr(storage, "SESSIONS_FILE", tmp_path / "sessions.json")
    return tmp_path


def test_register_and_login_doctor(isolated_store):
    doctor = storage.register_doctor("Jane Doe", "doc1", "secret")

    assert doctor is not None
    assert storage.login_doctor("doc1", "secret").name == "Jane Doe"
    assert storage.login_doctor("doc1", "wrong") is None
    assert storage.register_doctor("Jane Again", "doc1", "secret") is None


def test_patient_crud_and_search(isolated_store):
    patient = storage.save_patient(Patient("Alex Kim", "0700000000", "2001-01-01"))

    assert storage.get_patient_by_id(patient.patient_id).name == "Alex Kim"
    assert storage.search_patients_by_name("alex")[0].patient_id == patient.patient_id

    assert storage.update_patient(patient.patient_id, new_phone="0711111111")
    assert storage.get_patient_by_id(patient.patient_id).phone_number == "0711111111"

    assert storage.delete_patient(patient.patient_id)
    assert storage.get_patient_by_id(patient.patient_id) is None


def test_invalid_json_raises_clear_error(isolated_store):
    Path(storage.PATIENTS_FILE).write_text("{bad json", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON"):
        storage.get_all_patients()
