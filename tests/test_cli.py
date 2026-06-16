import main
import storage


def isolate(monkeypatch, tmp_path):
    monkeypatch.setattr(storage, "DOCTORS_FILE", tmp_path / "doctors.json")
    monkeypatch.setattr(storage, "PATIENTS_FILE", tmp_path / "patients.json")
    monkeypatch.setattr(storage, "DIAGNOSES_FILE", tmp_path / "diagnoses.json")
    monkeypatch.setattr(storage, "SESSIONS_FILE", tmp_path / "sessions.json")


def test_cli_register_add_and_list_patient(monkeypatch, tmp_path, capsys):
    isolate(monkeypatch, tmp_path)

    assert main.main(
        ["register-doctor", "--name", "Jane Doe", "--doctor-id", "doc1", "--password", "secret"]
    ) == 0
    assert main.main(
        [
            "add-patient",
            "--doctor-id",
            "doc1",
            "--password",
            "secret",
            "--name",
            "Alex Kim",
            "--phone",
            "0700000000",
            "--dob",
            "2001-01-01",
        ]
    ) == 0
    assert main.main(["list-patients"]) == 0

    output = capsys.readouterr().out
    assert "Alex Kim" in output


def test_cli_match_diagnosis(capsys):
    assert main.main(["match-diagnosis", "fever", "chills", "headache"]) == 0

    output = capsys.readouterr().out
    assert "Malaria" in output
