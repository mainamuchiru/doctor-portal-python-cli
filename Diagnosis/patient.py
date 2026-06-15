import json
import os
from typing import Optional, Dict, Any, List
from datetime import datetime

class Patient:
    """
    A class representing a Patient in the medical system.
    Handles patient data management and persistence using a JSON file.
    """
    
    FILE_PATH = "patients_data.json"

    def __init__(self, name: str, patient_id: str, date_of_birth: str, phone_number: str, 
                 height: Optional[float] = None, weight: Optional[float] = None):
        """
        Initialize a new Patient instance.
        
        :param name: Full name of the patient.
        :param patient_id: Unique identifier for the patient.
        :param date_of_birth: Date of birth in YYYY-MM-DD format.
        :param phone_number: Contact phone number.
        :param height: Height of the patient in cm (optional).
        :param weight: Weight of the patient in kg (optional).
        """
        self.name = name
        self.patient_id = patient_id
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
        self.height = height
        self.weight = weight
        
        # Ensure the JSON file exists
        self._ensure_file_exists()

    @classmethod
    def _ensure_file_exists(cls) -> None:
        """Private method to ensure the JSON database file exists."""
        if not os.path.exists(cls.FILE_PATH):
            with open(cls.FILE_PATH, 'w') as file:
                json.dump({}, file)

    def to_dict(self) -> Dict[str, Any]:
        """Convert patient attributes to a dictionary."""
        return {
            "name": self.name,
            "patient_id": self.patient_id,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "height": self.height,
            "weight": self.weight,
            "created_at": datetime.now().isoformat()
        }

    def add_new_patient(self) -> bool:
        """
        Save the current patient instance to the JSON file.
        
        :return: True if successful, False if patient_id already exists.
        """
        try:
            with open(self.FILE_PATH, 'r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {}

        if self.patient_id in data:
            print(f"Error: Patient with ID {self.patient_id} already exists.")
            return False

        data[self.patient_id] = self.to_dict()

        with open(self.FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
            
        print(f"Success: Patient {self.name} (ID: {self.patient_id}) added successfully.")
        return True

    @classmethod
    def fetch_patient_history(cls, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve patient details from the JSON file using patient_id.
        
        :param patient_id: The unique ID of the patient to fetch.
        :return: Dictionary containing patient details, or None if not found.
        """
        cls._ensure_file_exists()
        
        try:
            with open(cls.FILE_PATH, 'r') as file:
                data = json.load(file)
                
            if patient_id in data:
                print(f"Patient {patient_id} found. Fetching details...")
                return data[patient_id]
            else:
                print(f"Error: Patient with ID {patient_id} not found.")
                return None
                
        except json.JSONDecodeError:
            print("Error: Database file is corrupted.")
            return None

    @classmethod
    def list_all_patients(cls) -> List[Dict[str, Any]]:
        """Utility method to list all patients in the database."""
        cls._ensure_file_exists()
        try:
            with open(cls.FILE_PATH, 'r') as file:
                data = json.load(file)
            return list(data.values())
        except json.JSONDecodeError:
            return []

    def __str__(self) -> str:
        return f"Patient[{self.patient_id}]: {self.name}, DOB: {self.date_of_birth}"

class PatientDeleter:
    """
    A class specifically designed to handle the deletion of patient records.
    Ensures that deletion logic is decoupled from the main Patient data model.
    """
    
    @classmethod
    def delete_patient(cls, patient_id: str) -> bool:
        """
        Delete a patient from the JSON database.
        
        :param patient_id: ID of the patient to delete.
        :return: True if successfully deleted, False otherwise.
        """
        Patient._ensure_file_exists()
        
        try:
            with open(Patient.FILE_PATH, 'r') as file:
                data = json.load(file)
            
            if patient_id in data:
                patient_name = data[patient_id].get('name', 'Unknown')
                del data[patient_id]
                
                with open(Patient.FILE_PATH, 'w') as file:
                    json.dump(data, file, indent=4)
                
                print(f"Success: Patient {patient_name} (ID: {patient_id}) has been deleted.")
                return True
            else:
                print(f"Error: Patient with ID {patient_id} not found.")
                return False
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error: Could not access database for deletion. {e}")
            return False

# ==========================================
# Example Usage / Demo
# ==========================================
if __name__ == "__main__":
    # Clear existing file for a fresh demo
    if os.path.exists(Patient.FILE_PATH):
        os.remove(Patient.FILE_PATH)
        
    patients_to_add = [
        ("John Doe", "P1001", "1985-06-15", "+1-555-0101", 180.5, 75.0),
        ("Jane Smith", "P1002", "1992-11-23", "+1-555-0102", 165.0, 60.5),
        ("Robert Brown", "P1003", "1978-04-12", "+1-555-0103", 175.2, 82.1),
    ]

    print(f"Adding {len(patients_to_add)} patients to the database...")
    for name, pid, dob, phone, h, w in patients_to_add:
        p = Patient(name, pid, dob, phone, h, w)
        p.add_new_patient()

    print("-" * 40)
    print(f"Total patients before deletion: {len(Patient.list_all_patients())}")
    
    # Demonstrate deletion
    print("\nTesting PatientDeleter...")
    PatientDeleter.delete_patient("P1002")
    
    print("-" * 40)
    print(f"Total patients after deletion: {len(Patient.list_all_patients())}")
    
    # Verify P1002 is gone
    if not Patient.fetch_patient_history("P1002"):
        print("Verified: P1002 no longer exists in history.")
