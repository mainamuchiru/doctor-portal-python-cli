import json
import os
class StorageEngine:
    def __init__(self, kb_path="data/knowledge_base.json", diagnosis_path="data/diagnosis.json"):
        self.kb_path =kb_path# the kb is a variable representing knowledge_bae
        self.diagnosis_path= diagnosis_path

    def load_knowledge_base(self):
        if not os.path.exists(self.kb_path):
            print(f"[!] Warning: Knowlegde base file not found at {self.kb_path}")
            return{"diseases":[]}
        try:
            with open(self.kb_path,"r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("[!] Error: Malformed JSON data in knowledge base file.")
            return {"diseases":[]}
             
    def search_diseases_by_symptom(self, symptom_query):
        query= symptom_query.strip().lower()# the strip cleans the whitespace
        matches=[]

        kb_data=self.load_knowledge_base()
        diseases=kb_data.get("diseases",[])  

        for disease in diseases:
            symptoms_lowercase=[s.lower() for s in disease.get("symptoms",[])]
            if any(query in symptom for symptom in symptoms_lowercase):
                matches.append(disease)
        return matches

    def save_diagnosis(self,diagnosis_data):
        # Read existing records 
        records = []
        if os.path.exists(self.diagnosis_path):
            try:
                with open(self.diagnosis_path,"r") as file:
                    records = json.load(file)
                    if not isinstance(records,list):
                        records=[]
            except (json.JSONDecodeError, IOError):
                records=[]
                # Appends the new diagnostic record            
        records.append(diagnosis_data)
        # Write the updated history back to the file
        try:
            with open(self.diagnosis_path,"w") as file:
                json.dump(records,file,indent=4)
                return True
        except IOError as e:
            print(f"[!] File Write Error: Could not save diagnosis history. Details: {e}") 
            return False    
    def load_patient(self, patient_id):
        """Placeholder method to satisfy Doctor class requirements.In a full implementation, this reads patient profile details from a file"""
        return None    
