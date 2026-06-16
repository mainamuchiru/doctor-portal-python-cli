from abc import ABC, abstractmethod
from typing import Dict, Any

class User(ABC):
    """
    Base class for all users in the system.
    Demonstrates inheritance and encapsulation.
    """
    def __init__(self, name: str, user_id: str, password_hash: str, role: str):
        self._name = name.strip()
        self._user_id = user_id.strip()
        self._password_hash = password_hash
        self._role = role

    @property
    def name(self) -> str:
        return self._name

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def role(self) -> str:
        return self._role

    def check_password(self, password_input: str) -> bool:
        from utils.auth import hash_password
        return self._password_hash == hash_password(password_input)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
