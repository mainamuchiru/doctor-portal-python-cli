import json
import random
import uuid
from pathlib import Path
from datetime import datetime, timedelta

# Mock data for generation
NAMES = ["John Doe", "Jane Smith", "Robert Brown", "Emily Davis", "Michael Wilson", 
         "Sarah Miller", "David Taylor", "Jessica Moore", "William Anderson", "Elizabeth Thomas",
         "Chris Jackson", "Ashley White", "Matthew Harris", "Linda Martin", "Joseph Thompson",
         "Susan Garcia", "Thomas Martinez", "Margaret Robinson", "Charles Clark", "Dorothy Rodriguez"]

DISEASES = ["Malaria", "Hypertension", "Typhoid Fever", "Common Cold", "Pneumonia", "Diabetes"]

def generate_data():
    data_dir = Path("json_data")
    data_dir.mkdir(exist_ok=True)
    
    # Generate 20 Doctors
    doctors = {}
    from utils.auth import hash_password
    for i in range(1, 21):
        doc_id = f"DOC{1000+i}"
        doctors[doc_id] = {
            "name": f"Dr. {NAMES[i-1]}",
            "doctor_id": doc_id,
            "password": hash_password("password123"),
            "role": "doctor"
        }
    # Add an admin
    doctors["admin1"] = {
        "name": "System Admin",
        "admin_id": "admin1",
        "password": hash_password("adminpass"),
        "role": "admin"
    }
    
    with open(data_dir / "doctors.json", "w") as f:
        json.dump(doctors, f, indent=4)

    # Generate 20 Patients
    patients = {}
    patient_ids = []
    for i in range(1, 21):
        p_id = f"PAT{2000+i}"
        patient_ids.append(p_id)
        patients[p_id] = {
            "name": NAMES[random.randint(0, 19)],
            "patient_id": p_id,
            "date_of_birth": (datetime.now() - timedelta(days=random.randint(7000, 20000))).strftime("%Y-%m-%d"),
            "phone_number": f"+1-555-01{i:02d}",
            "height": str(random.randint(150, 200)),
            "weight": str(random.randint(50, 100))
        }
    
    with open(data_dir / "patients.json", "w") as f:
        json.dump(patients, f, indent=4)

    # Generate 20 Sessions and Diagnoses
    sessions = {}
    diagnoses = {}
    doc_list = list(doctors.keys())
    
    for i in range(1, 21):
        s_id = str(uuid.uuid4())
        p_id = patient_ids[i-1]
        d_id = doc_list[random.randint(0, 19)]
        disease = random.choice(DISEASES)
        
        sessions[s_id] = {
            "session_id": s_id,
            "patient_id": p_id,
            "doctor_id": d_id,
            "diagnosis": disease,
            "status": "completed",
            "date_time": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "notes": [{"timestamp": datetime.now().isoformat(), "note": "Regular checkup"}],
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat()
        }
        
        diagnoses[s_id] = {
            "session_id": s_id,
            "patient_id": p_id,
            "doctor_id": d_id,
            "symptoms": ["fever", "headache"],
            "disease": disease,
            "prevention": "Rest and fluids",
            "medication": "Consult pharmacist"
        }

    with open(data_dir / "sessions.json", "w") as f:
        json.dump(sessions, f, indent=4)
        
    with open(data_dir / "diagnoses.json", "w") as f:
        json.dump(diagnoses, f, indent=4)

    print("Successfully generated 20+ records for each file in json_data/")

if __name__ == "__main__":
    generate_data()
