import Diagnosis.storage as storage
from Diagnosis.session import Session
from Diagnosis.diagnosis import Diagnosis
from utils.utils import prompt, header


def diagnose_patient(doctor):
    header("Diagnose Patient")

    patient_name = prompt("Patient Name: ")
    if not patient_name:
        print("[!] A patient name is required to start a session.")
        return

    patient = storage.get_patient_by_name(patient_name)
    if not patient:
        print(f"[!] No patient found with name: {patient_name}")
        return

    print(f"\nStarting session for {patient.name}...")

    session = Session(patient.patient_id, doctor.doctor_id)

    start_time = session.start_time()
    print(f"[OK] Session started at {start_time}")

    diag = Diagnosis(
        session.session_id,
        patient.patient_id,
        doctor.doctor_id
    )

    confirmed = diag.enter_symptoms(storage)

    if confirmed:
        session.diagnosis = diag.disease
        diag.show_summary()

        note = prompt("Notes: ")
        if note:
            session.record_notes(note)

        end_time = session.end_time()
        print(f"[OK] Session ended at {end_time}")

        storage.save_diagnosis(diag.to_dict())
        storage.save_session(session.to_dict())

        print("[OK] Session and diagnosis saved successfully.")
    else:
        session.update_status("cancelled")
        session.end_time()
        storage.save_session(session.to_dict())
        print("[!] Diagnosis was not completed. Session cancelled.")