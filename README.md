# Doctor Portal Python CLI

A modular command-line doctor portal for managing doctors, patients, sessions, and diagnosis suggestions with JSON persistence.It Allows doctors to register, add patients, and match diagnoses based on symptoms.It is designed to be simple, extensible, and easy to use. This project is built using Python and follows a modular architecture, making it easy to maintain and extend.This project in a real world scenario can be used by doctors /major health practitioners to manage their patients and provide diagnosis suggestions based on symptoms.

## Technologies Used

* **Python 3.8+**
* **Click** - For building the interactive command-line interface
* **JSON** - For lightweight data persistence
* **Pytest** - For robust unit testing
* **Logging** - For debugging and application monitoring

---

# The structure of the project is as follows:

## Project Structure

## Project Structure

```text
doctor-portal-python-cli/
├── diagnosis/
│   ├── __init__.py
│   └── diagnosis.py
├── doctor/
│   ├── __init__.py
│   └── doctor.py
├── json/
│   ├── diagnoses.json
│   ├── doctors.json
│   ├── knowledge_base.json
│   ├── patients.json
│   └── session_state.json
├── menu/
│   ├── __init__.py
│   ├── auth_menu.py
│   ├── doctor_menu.py
│   ├── main_menu.py
│   ├── patient_menu.py
│   └── session_menu.py
├── tests/
│   ├── test_all_files_present.py
│   ├── test_cli.py
│   ├── test_models.py
│   └── test_storage.py
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── main.py
├── README.md
├── requirements.txt
└── utils.py
```

# Using pip
pip install -r requirements.txt

# Using pipenv
pipenv install
pipenv shell

## VIDEO 
This video below explains the project structure, how to run the application, and how to execute tests.

[![Doctor Portal Python CLI]()]

## Running the Application

You can execute commands using the following syntax:

```bash
python main.py [COMMAND] [OPTIONS]
# Register a new doctor
python main.py register-doctor --name "Jane Doe" --doctor-id doc1 --password secret

# Add a patient under a specific doctor
python main.py add-patient --doctor-id doc1 --password secret --name "Alex Kim" --phone "0700000000" --dob "2001-01-01"

# List all patients
python main.py list-patients

# Match a diagnosis based on a list of symptoms
python main.py match-diagnosis fever chills headache

# Start the interactive CLI mode
python main.py interactive
```
#  Running Tests
Python - `pytest tests/`
