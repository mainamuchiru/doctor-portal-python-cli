from session import Session


def main():
   

    # ── Create sessions ──────────────────────────────
    print("\n--- Creating Sessions ---")
    # Option A: uses default 'session.json'
    s1 = Session(patient_id="P001", doctor_id="D101", diagnosis="Hypertension")

    # Option B: point to a custom file path
    # s1 = Session(patient_id="P001", doctor_id="D101", diagnosis="Hypertension", storage_file="data/session.json")

    s2 = Session(patient_id="P002", doctor_id="D101", diagnosis="Diabetes")
    s3 = Session(patient_id="P001", doctor_id="D202", diagnosis="Flu")


if __name__ == "__main__":
    main()
