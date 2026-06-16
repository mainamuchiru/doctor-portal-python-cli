from models.user import User
from typing import Dict, Any

class Doctor(User):
    def __init__(self, name: str, doctor_id: str, password_hash: str):
        super().__init__(name, doctor_id, password_hash, role="doctor")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "doctor_id": self.user_id,
            "password": self._password_hash,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Doctor":
        return cls(data["name"], data["doctor_id"], data["password"])

class Admin(User):
    def __init__(self, name: str, admin_id: str, password_hash: str):
        super().__init__(name, admin_id, password_hash, role="admin")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "admin_id": self.user_id,
            "password": self._password_hash,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Admin":
        return cls(data["name"], data["admin_id"], data["password"])
