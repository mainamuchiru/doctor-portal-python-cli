from session import Session


def create_session():
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")
    diagnosis = input("Enter diagnosis (optional): ")

    session = Session(patient_id, doctor_id, diagnosis)

    print("\nSession created successfully.")
    print(session)


def view_sessions():
    sessions = Session.load_all_sessions()

    if not sessions:
        print("\nNo sessions found.")
        return

    print("\n--- Sessions ---")
    for session in sessions:
        print(f"Session ID : {session['session_id']}")
        print(f"Patient ID : {session['patient_id']}")
        print(f"Doctor ID  : {session['doctor_id']}")
        print(f"Status     : {session['status']}")
        print(f"Diagnosis  : {session['diagnosis']}")
        print("-" * 30)


def update_status():
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")

    session = Session(patient_id, doctor_id)

    status = input(
        "Enter status (referred/in-progress/completed/cancelled): "
    )

    try:
        session.update_status(status)
    except ValueError as error:
        print(error)


def add_note():
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")

    session = Session(patient_id, doctor_id)

    note = input("Enter note: ")
    session.record_notes(note)


def start_session():
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")

    session = Session(patient_id, doctor_id)
    session.start_time()


def end_session():
    patient_id = input("Enter patient ID: ")
    doctor_id = input("Enter doctor ID: ")

    session = Session(patient_id, doctor_id)

    try:
        session.start_time()
        session.end_time()
    except RuntimeError as error:
        print(error)