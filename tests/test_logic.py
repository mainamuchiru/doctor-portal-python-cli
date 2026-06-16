import pytest
from utils.auth import hash_password
from models.doctor import Doctor

def test_password_hashing():
    password = "secret_password"
    h1 = hash_password(password)
    h2 = hash_password(password)
    assert h1 == h2
    assert h1 != password

def test_doctor_inheritance():
    doc = Doctor("House", "house1", hash_password("pass"))
    assert doc.name == "House"
    assert doc.role == "doctor"
    assert doc.check_password("pass") is True
    assert doc.check_password("wrong") is False
