from typing import Any, Dict


class Doctor:
    """Doctor account with simple password checking."""

    def __init__(self, name: str, doctor_id: str, password: str) -> None:
        self.name = name.strip()
        self.doctor_id = doctor_id.strip()
        self._password = password

    @property
    def password(self) -> str:
        return self._password

    def check_password(self, password_input: str) -> bool:
        return self._password == password_input

    def update(self, name: str = "", password: str = "") -> None:
        if name:
            self.name = name.strip()
        if password:
            self._password = password

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Doctor":
        return cls(data["name"], data["doctor_id"], data["password"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "doctor_id": self.doctor_id,
            "password": self._password,
        }
