class Diagnosis:
    def __init__(self,session_id,patient_id,doctor_id):
        self.session_id=session_id
        self.patient_id=patient_id
        self.doctor_id=doctor_id

        #tHIS WILL DO THE INPUTS
        self._symptoms= ""
        self._disease= ""
        self._prevention= ""
        self._medication= ""
# ================================================    
#   GETTERS AND SETTERS (Class Level Indentation)
# ================================================
    @property
    def symptoms(self):
        """Getter: Safely returns the entered symptoms"""
        return self._symptoms

    @symptoms.setter
    def symptoms(self, value):
        """Setter: Ensures symptoms is a non-empty string"""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("[!] Invalid data: Symptoms must be a valid text string")
        self._symptoms = value.strip()

    @property
    def disease(self):
        """Getter: Safely returns the clinical condition name"""
        return self._disease

    @disease.setter
    def disease(self, value):
        """Setter: Ensures the disease value is a non-empty string."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("[!] Invalid data: Disease name must be a valid text string")
        self._disease = value.strip()

    @property
    def prevention(self):
        """Getter: Safely returns the prevention plan"""
        return self._prevention

    @prevention.setter
    def prevention(self, value):
        """Setter: Strips whitespace automatically when prevention is assigned"""
        self._prevention = value.strip() if isinstance(value, str) else value

    @property
    def medication(self):
        """Getter: Safely returns the treatment medication plan"""
        return self._medication

    @medication.setter
    def medication(self, value):
        """Setter: Strips whitespace automatically when medication is assigned"""
        self._medication=value.strip() if isinstance(value, str) else value # This is a ternary operator 
    @property
    def symptoms(self):
        return self._symptoms
    @symptoms.setter
    def symptoms(self,value):
        self._symptoms = value 
    @property
    def prevention(self):
        return self._prevention
    @prevention.setter
    def prevention(self,value):
        self._prevention = value.strip() if isinstance(value,str) else value              

#=====================================================
# CORE METHOD UTILITIES
# =====================================================

      #This is where when the doctor inputs symptoms to triggr the search
    def enter_symptoms(self,storage_engine):
        symptom=input("Enter symptom to search: ")
        self.symptoms = symptom # This saves the string into your class attribute!
 
        matches=storage_engine.search_diseases_by_symptom(self._symptoms)
        print("\nMatching Diseases Found")
        if not matches:
            print("[!] No matching diseases found for that symptom. Please try again")
            return False

        for index, disease in enumerate(matches, start=1):
            print(f"{index}. {disease['name']}")
        try:
            choice = int(input("\nSelect the matching disease number: "))
            if 1<=choice<=len(matches):
                selected_disease=matches[choice -1]
                self.disease= selected_disease["name"]
                self.prevention=selected_disease["prevention"]
                self.medication= selected_disease["medication"]
                
                print(f"[tick]Diagnosis confirm: {self.disease}")
                return True

                print(f"[tick] Diagnosis confirmed: {self.disease}")
                return True
            else:
                print("[!] Invalid selection number.")
                return False

        except ValueError:
            print("[!] Invalid input.  Please enter a valid number.")
        return False                

      # To show what has been tracked  
    def display_symptoms(self):
        """Display a summary of the current session details"""
        print("\n" + "=" * 40)
        print(f"DIAGNOSIS SUMMARY (Session: {self.session_id})")
        print("="*40) 
        print(f"Patient ID: {self.patient_id}") 
        print(f"Doctor ID: {self.doctor_id}") 
        print(f"Symptom: {self.symptoms}") 
        print(f"Condition: {self.disease}") 
        print(f"Prevention: {self.prevention}") 
        print(f"Medication: {self.medication}")        
      
      # To format everything cleanly into a dictionary and sen it to the StorageEngine.save_diagnosis()  
    def save_diagnosis(self, storage_engine):
        """Bundles the session details into a dict and pushes to storage.py"""
        if not self.disease:
            print("[!] Cannot save an incomplete diagnosis session.")
            return False
        return storage_engine.save_diagnosis(self.to_dict())

        diagnosis_data = self.to_dict()  # FIX: was missing — caused unreachable return
        return storage_engine.save_diagnosis(diagnosis_data)

    def show_summary(self):
        print("\n" + "=" * 40)
        print("DIAGNOSIS SUMMARY")
        print("=" * 40)
        print("Session ID :", self.session_id)
        print("Patient ID :", self.patient_id)
        print("Doctor ID  :", self.doctor_id)
        print("Symptoms   :", self.symptoms)
        print("Disease    :", self.disease)
        print("Prevention :", self.prevention)
        print("Medication :", self.medication)
        print("=" * 40)

    def to_dict(self): # This returns the information more of displaying
        return {
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": self.symptoms,
            "disease": self.disease,
            "prevention": self.prevention,
            "medication": self.medication
        }   
