import json
import os
import uuid
from datetime import datetime


class Session:
    STORAGE_FILE = "session.json"

    def __init__(self, patient_id, doctor_id, diagnosis="", date_time=None):
        self.session_id = str(uuid.uuid4())
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.status = "scheduled"
        self.date_time = (date_time or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.notes = []
        self._start_time = None
        self._end_time = None

        self._save_to_json()


    def _load_all(self):
        
        if not os.path.exists(self.STORAGE_FILE):
            return {}
        with open(self.STORAGE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _save_to_json(self):
        
        all_sessions = self._load_all()
        all_sessions[self.session_id] = self._to_dict()
        with open(self.STORAGE_FILE, "w") as f:
            json.dump(all_sessions, f, indent=4)
        print(f"[Storage] Session {self.session_id} saved to '{self.STORAGE_FILE}'")

    def _to_dict(self):
        
        return {
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "diagnosis": self.diagnosis,
            "status": self.status,
            "date_time": self.date_time,
            "notes": self.notes,
            "start_time": self._start_time,
            "end_time": self._end_time,
        }

    

    def update_status(self, new_status):
        valid_statuses = ["scheduled", "in-progress", "completed", "cancelled"]
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self.status = new_status
        self._save_to_json()
        print(f"Status updated to: {self.status}")

    def record_notes(self, note):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.notes.append({"timestamp": timestamp, "note": note})
        self._save_to_json()
        print(f"Note recorded at {timestamp}")

    def start_time(self):
        self._start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_status("in-progress")
        print(f"Session started at: {self._start_time}")
        return self._start_time

    def end_time(self):
        if not self._start_time:
            raise RuntimeError("Session has not been started yet.")
        self._end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_status("completed")
        print(f"Session ended at: {self._end_time}")
        return self._end_time

    

    @classmethod
    def search_session(cls, **criteria):
        
        if not os.path.exists(cls.STORAGE_FILE):
            print("No storage file found.")
            return []
        with open(cls.STORAGE_FILE, "r") as f:
            all_sessions = json.load(f)
        return [
            s for s in all_sessions.values()
            if all(s.get(k) == v for k, v in criteria.items())
        ]

    @classmethod
    def load_all_sessions(cls):
       
        if not os.path.exists(cls.STORAGE_FILE):
            return []
        with open(cls.STORAGE_FILE, "r") as f:
            return list(json.load(f).values())

    def __repr__(self):
        return (
            f"Session(id={self.session_id}, patient={self.patient_id}, "
            f"doctor={self.doctor_id}, status={self.status}, "
            f"date={self.date_time})"
        )
