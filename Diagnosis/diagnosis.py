# This basically is a file that will work on the symptom when the doctor enters the symptoms of the patient
#There is the search bar -  this is where the doctor has to write the symptoms
#There is the display diagnosis - once the doctor enters the symptoms it will go to the diagnosis.json where the most likely disease is captured and displayed on the terminal{name,symptoms,preventions and medication}
#There is the save diagnosis
class Diagnosis:
      def __init__(self,session_id,patient_id,doctor_id):
        self.session_id=session_id
        self.patient_id=patient_id
        self.doctor_id=doctor_id

        #tHIS WILL DO THE INPUTS
        self._symptoms=""
        self._disease=""
        self._prevention=""
        self._medication=""
# ================================================    
#   GETTERS AND SETTERS (Class Level Indentation)
# ================================================
    @property
    def disease(self):
        """Getter: Safely returns the clinical condition name"""
        return self._disease

    @disease.setter
    def disease(self, value):
        """ Setter: Ensures the disease value is a non-empty string."""
        if not isinstance(value, str) or value.strip()="":
                raise ValueError("[!] Invalid data: Disease name must be a valid text string ")
            self._disease=value.strip()

    @property
    def medication(self):
        """Getter: Safely returns the treatment medication plan"""
        return self._medication

    @medication.setter  
    def medication(self, value):
        """Setter: Strips whitespace automatically when medication is assigned"""
        self._medication=value.strip() if isinstance(value, str) else value # This is a ternary operator 
          
#=====================================================
# CORE METHOD UTILITIES
#=====================================================

      #This is where when the doctor inputs symptoms to triggr the search
      def enter_symptoms(self,storage_engine):
        symptom=input("Enter symptom to search: ")
        self._symptoms = symptom # This saves the string into your class attribute!
 
        matches=storage_engine.search_diseases_by_symptom(self.symptoms)
        print("\nMatching Diseases Found")
        if not matches:
            print("[!] No matching diseases found for that symptom.Please try again")
            return False

        for index, disease in enumerate(matches, start=1):
            print(f"{index}. {disease['name']}")
        try:
            choice = int(input("\nSelect the matching disease number: "))
            if 1<=choice<=len(matches):
                selected_disease=matches[choice -1]
                self.disease= selected_disease["name"]
                self.prevention=selected_disease["prevention"]
                self._medication= selected_disease["medication"]
                
                print(f"[tick]Diagnosis confirm: {self.disease}")
                return True

            else:
                print(F"[!]Invalid selection number.")
                return False

        except ValueError:
            print("[!] Invalid Please eneter a valid number.")
            return False                

      # To show what has been tracked  
      def display_symptoms(self):
        """Display a summary of the current session details"""

        print("\n"+"="*40)
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
        diagnosis_data={
            "session_id": self.session_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "symptoms": self.symptoms,
            "disease": self.disease,
            "prevention": self.prevention,
            "medication": self.medicaion
        }    
        return storage_engine.save_diagnosis(diagnosis_data)
