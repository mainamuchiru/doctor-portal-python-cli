import json
import os
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime

class Patient:
    """
    A class representing a Patient in the medical system.
    """
    
    def __init__(self, name: str, phone_number: str, date_of_birth: str, 
                 height: str = "", weight: str = "", patient_id: Optional[str] = None):
        self.name = name.strip()
        self.phone_number = phone_number.strip()
        self.date_of_birth = date_of_birth.strip()
        self.height = height
        self.weight = weight
        self.patient_id = patient_id or str(uuid.uuid4())[:8].upper()

    def validate(self) -> None:
        if not self.name:
            raise ValueError("Patient name is required.")
        if not self.phone_number:
            raise ValueError("Phone number is required.")
        if not self.date_of_birth:
            raise ValueError("Date of birth is required.")

    def update(self, name: str = "", phone: str = "", dob: str = "", height: str = "", weight: str = "") -> None:
        if name:
            self.name = name.strip()
        if phone:
            self.phone_number = phone.strip()
        if dob:
            self.date_of_birth = dob.strip()
        if height:
            self.height = height
        if weight:
            self.weight = weight

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Patient":
        return cls(
            name=data["name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            height=data.get("height", ""),
            weight=data.get("weight", ""),
            patient_id=data["patient_id"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "patient_id": self.patient_id,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "height": self.height,
            "weight": self.weight,
        }

    def save(self) -> "Patient":
        """Persist the current patient instance to storage."""
        from data import storage
        return storage.save_patient(self)

    @classmethod
    def get_all(cls) -> List["Patient"]:
        """Retrieve all patients from storage."""
        from data import storage
        return storage.get_all_patients()

    @classmethod
    def get_by_id(cls, patient_id: str) -> Optional["Patient"]:
        """Find a specific patient by their ID."""
        from data import storage
        return storage.get_patient_by_id(patient_id)

    def delete(self) -> bool:
        """Remove the current patient from storage."""
        from data import storage
        return storage.delete_patient(self.patient_id)

    def __str__(self) -> str:
        return f"Patient[{self.patient_id}]: {self.name}, DOB: {self.date_of_birth}"
