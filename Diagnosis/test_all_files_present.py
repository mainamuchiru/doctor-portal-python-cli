import sys
import os
from doctor import Doctor
from patient import Patient
from diagnosis import Diagnosis
from session import Session
from StorageEngine import StorageEngine

def run_system_diagnostic():
    print("=" * 50)
    print("     SYSTEM VERIFICATION RUN    ")
    print("=" * 50)
    try:
        print("[1/4] Connecting to Database Engines...")
        storage=StorageEngine(kb_path="knowledge_base_json", diagnosis_path="session.json")
        print("\n[2/4] Loading Mock Profiles into Actice RAM Memory...")
        active_doctor = Doctor(name="Alice Mwenda", doctor_id="D101", password="docpass")
        active_patient=Patient(name="ann",phone_number="987674" date_of_birth=1990-11-05)
        print(f"  -> Doctor recognized: {active_doctor.name}")
        print(f"  -> Patient baseline string: {active_patient}")

        print("\n[3/4] Initializing Live Clinical Encounter Timer...")
        clinical_session = Session(
            patient_id=active_patient.patient_id,
            doctor_id=active_doctor.doctor_id,
            diagnosis ="Malaria"        
        )
        
        clinical_session.start_time()
        clinical_session.add_note("Consultation tracking running normally.")
        clinical_session.end_time()
        print("\n[4/4] Evaluating symptoms Diagnostics Pipeline...")
        search_target="fever"
        matches=storage.search_diseases_by_symptom(search_target)
        print(f"     -> Searching Knowledge base for '{search_target}': Found {len(matches)} matches. ")
        
        medical_record=Diagnosis(
            session_id=clinical_session.session_id,
            patient=active_patient.patient_id,
            doctor_id=active_doctor.doctor_id
        )
        if matches:
            matched_disease=matches[0]
            medical_record.disease=matched_disease["name"]
            medical_record.prevention=matched_disease["prevention"]
            medical_record.medication = matched_disease["medication"]

            medical_record.show_summary()
            print("\n[*] Saving diagnosis object using file interface connection...")
            save_success=medical_record.save_diagnosis(storage)

            if save_success:
                print("\n==== [SUCCESS]==== ")
        else:   
                print("\n[!] File pipeline failed to write the records payload.") 
    except Exception as runtime_error:
            print(f"\nCRITICAL RUNTIME ERROR LOCATED: {runtime_error}", file=sys.stderr)
            sys.exit(1)        
if __name__=="__main__":
    run_system_diagnostic()            