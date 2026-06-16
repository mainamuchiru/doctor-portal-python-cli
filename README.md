# Doctor Portal Python CLI

A modular command-line doctor portal for managing doctors, patients, sessions, and diagnosis suggestions with JSON persistence.

## Common commands

```bash
python main.py register-doctor --name "Jane Doe" --doctor-id doc1 --password secret
python main.py add-patient --doctor-id doc1 --password secret --name "Alex Kim" --phone "0700000000" --dob "2001-01-01"
python main.py list-patients
python main.py match-diagnosis fever chills headache
python main.py interactive
```

## Tests

```bash
python -m pytest
```
