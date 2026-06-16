# List of diseases with symptoms, prevention and medication
DISEASES = [
    {
        "name": "Malaria",
        "symptoms": ["fever", "chills", "headache", "nausea", "vomiting", "muscle pain"],
        "prevention": "Use mosquito nets, insect repellent, antimalarial drugs.",
        "medication": "Artemether-Lumefantrine, Chloroquine"
    },
    {
        "name": "Hypertension",
        "symptoms": ["headache", "dizziness", "chest pain", "blurred vision", "nausea"],
        "prevention": "Reduce salt intake, exercise regularly, avoid stress.",
        "medication": "Amlodipine, Lisinopril"
    },
    {
        "name": "Typhoid Fever",
        "symptoms": ["high fever", "headache", "stomach pain", "diarrhea", "rash", "vomiting"],
        "prevention": "Safe drinking water, proper sanitation, typhoid vaccine.",
        "medication": "Ciprofloxacin, Azithromycin"
    },
    {
        "name": "Common Cold",
        "symptoms": ["runny nose", "sore throat", "sneezing", "cough", "mild fever"],
        "prevention": "Wash hands frequently, avoid sick people.",
        "medication": "Rest, fluids, Paracetamol"
    },
    {
        "name": "Pneumonia",
        "symptoms": ["chest pain", "cough", "fever", "shortness of breath", "chills"],
        "prevention": "Pneumococcal vaccine, good hygiene, avoid smoking.",
        "medication": "Amoxicillin, Azithromycin"
    },
    {
        "name": "Diabetes",
        "symptoms": ["frequent urination", "excessive thirst", "fatigue", "blurred vision", "slow healing"],
        "prevention": "Healthy weight, balanced diet, regular exercise.",
        "medication": "Metformin, Insulin"
    },
]


class Diagnosis:
    def __init__(self, session_id, patient_id, doctor_id):
        self.session_id = session_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.symptoms = []
        self.disease = ""
        self.prevention = ""
        self.medication = ""

    def search_diseases(self, symptom):
        # search through the DISEASES list and return matches
        results = []
        for disease in DISEASES:
            for s in disease["symptoms"]:
                if symptom.lower() in s.lower():
                    results.append(disease)
                    break  # no need to check other symptoms of same disease
        return results

    @staticmethod
    def match_symptoms(symptoms):
        """Return diseases ranked by how many supplied symptoms they match."""
        cleaned = [symptom.lower().strip() for symptom in symptoms if symptom.strip()]
        ranked = []

        for disease in DISEASES:
            matches = []
            for symptom in cleaned:
                for known_symptom in disease["symptoms"]:
                    if symptom in known_symptom.lower() or known_symptom.lower() in symptom:
                        matches.append(known_symptom)
                        break
            if matches:
                ranked.append(
                    {
                        "name": disease["name"],
                        "matched_symptoms": sorted(set(matches)),
                        "score": len(set(matches)),
                        "prevention": disease["prevention"],
                        "medication": disease["medication"],
                    }
                )

        return sorted(ranked, key=lambda item: item["score"], reverse=True)

    def enter_symptoms(self):
        print("\nEnter between 3 and 5 symptoms for the patient.")
        all_matches = {}  # use dict to avoid duplicates

        for i in range(1, 6):
            symptom = input(f"Symptom {i}: ").strip()

            if symptom == "" and i > 3:
                # doctor pressed enter with no input after 3 symptoms, stop
                break
            elif symptom == "" and i <= 3:
                print("Please enter at least 3 symptoms.")
                i -= 1  # try same number again
                continue

            self.symptoms.append(symptom)

            # search for matching diseases
            matches = self.search_diseases(symptom)
            for disease in matches:
                all_matches[disease["name"]] = disease

            # after 3 symptoms ask if they want to add more
            if i >= 3:
                more = input("Add another symptom? (y/n): ").strip().lower()
                if more == "n":
                    break

        if len(all_matches) == 0:
            print("No matching diseases found for the entered symptoms.")
            return False

        # show the doctor the possible diseases
        disease_list = list(all_matches.values())
        print("\nPossible conditions based on symptoms entered:")
        print("-" * 40)
        for i, d in enumerate(disease_list, 1):
            print(f"{i}. {d['name']}")

        # let doctor pick the confirmed disease
        try:
            choice = int(input("\nSelect the correct condition number: "))
            if 1 <= choice <= len(disease_list):
                selected = disease_list[choice - 1]
                self.disease = selected["name"]
                self.prevention = selected["prevention"]
                self.medication = selected["medication"]
                print("Diagnosis confirmed:", self.disease)
                return True
            else:
                print("Invalid number selected.")
                return False
        except ValueError:
            print("Please enter a valid number.")
            return False

    def show_summary(self):
        print("\n" + "=" * 40)
        print("DIAGNOSIS SUMMARY")
        print("=" * 40)
        print("Session ID :", self.session_id)
        print("Patient ID :", self.patient_id)
        print("Doctor ID  :", self.doctor_id)
        print("Symptoms   :", ", ".join(self.symptoms))
        print("Disease    :", self.disease)
        print("Prevention :", self.prevention)
        print("Medication :", self.medication)
        print("=" * 40)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": self.symptoms,
            "disease": self.disease,
            "prevention": self.prevention,
            "medication": self.medication
        }
