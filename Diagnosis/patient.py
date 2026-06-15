from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4


class Record:
    """Base class for stored records."""

    def __init__(self, record_id: Optional[str] = None) -> None:
        self.record_id = record_id or str(uuid4())
        self.created_at = datetime.now().isoformat(timespec="seconds")


class Patient(Record):
    """Patient profile used by the doctor portal."""

    def __init__(
        self,
        name: str,
        phone_number: str,
        date_of_birth: str,
        height: str = "",
        weight: str = "",
        patient_id: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> None:
        super().__init__(patient_id)
        self.patient_id = self.record_id
        self.name = name.strip()
        self.phone_number = phone_number.strip()
        self.date_of_birth = date_of_birth.strip()
        self.height = str(height).strip() if height is not None else ""
        self.weight = str(weight).strip() if weight is not None else ""
        if created_at:
            self.created_at = created_at

    def validate(self) -> None:
        missing = []
        if not self.name:
            missing.append("name")
        if not self.phone_number:
            missing.append("phone number")
        if not self.date_of_birth:
            missing.append("date of birth")
        if missing:
            raise ValueError("Missing required patient field(s): " + ", ".join(missing))

    def update(
        self,
        name: str = "",
        phone_number: str = "",
        date_of_birth: str = "",
        height: str = "",
        weight: str = "",
    ) -> None:
        if name:
            self.name = name.strip()
        if phone_number:
            self.phone_number = phone_number.strip()
        if date_of_birth:
            self.date_of_birth = date_of_birth.strip()
        if height:
            self.height = str(height).strip()
        if weight:
            self.weight = str(weight).strip()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Patient":
        return cls(
            name=data["name"],
            phone_number=data["phone_number"],
            date_of_birth=data["date_of_birth"],
            height=data.get("height", ""),
            weight=data.get("weight", ""),
            patient_id=data.get("patient_id"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "phone_number": self.phone_number,
            "date_of_birth": self.date_of_birth,
            "height": self.height,
            "weight": self.weight,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        return f"{self.name} ({self.patient_id})"


class PatientDeleter:
    """Small service class for deleting patients through storage."""

    @staticmethod
    def delete_patient(patient_id: str) -> bool:
        import storage

        return storage.delete_patient(patient_id)
