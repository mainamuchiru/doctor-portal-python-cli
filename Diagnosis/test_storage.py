import unittest
import os
import json 
from storage import StorageEngine

class TestStorageSystem(unittest.TestCase):
    def setUp(self):
        """Creates isolated temporary files for testing to protect production data. """
        self.test_kb_file="test_knowledge_base.json"
        self.test_diagnosis_file="test_session.json"

        self.dummy_kb_data = {
            "diseases": [
                {
                    "name": "Malaria",
                    "symptoms":["fever","chills"],
                    "prevention": "Use nets",
                    "medication": "ACT"
                }
            ]
        }
        with open(self.test_kb_file,"w", encoding="utf-8") as f:
            json.dump(self.dummy_kb_data,f)

        self.storage= StorageEngine(kb_path=self.test_kb_file,diagnosis_path=self.test_diagnosis_file)
   
    def tearDown(self):
        """Cleans up and deletes temporary test workspace logs."""
        if os.path.exists(self.test_kb_file):
            os.remove(self.test_kb_file)
        if os.path.exists(self.test_diagnosis_file):
            os.remove(self.test_diagnosis_file)
#============================================================
#HAPPY PATH
#============================================================
    def test_load_diagnosis_History(self):
        """Verify that the storage engine successfully reads data from JSON"""
        data = self.storage.load_diagnosis_History()
        self.assertIn("diseases",data)
        self.assertEqual(data["diseases"][0]["name"],"Malaria") 

    def test_search_diseases_by_symptoms(self):
        """Verifies symptoms keyword matching filter results correctly and case-insensitively"""
         matches = self.storage.search_diseases_by_symptom("FEVER") 
         self.assertEqual(len(matches),1)
         self.assertEqual(matches[0]["name"],"Malaria")

    def test_save_diagnosis_persistence(self):
        """ Verifies writing and appending active diagnosis records to the file system. """
          mock_payload = {
            "session_id": "MOCK-SESS-99",
            "patient_id":"p-7f315f",
            "doctor_id":"D101",
            "symptoms": ["fever"],
            "disease": "Malaria"
          }     
        status = self.storage.save_diagnosis(mock_payload)
        self.assertTrue(status)
        
        with open(self.test_diagnosis_file, "r", encoding="utf-8") as file:
            saved_records= json.load(file)

            self.assertEqual(len(saved_records),1)
            self.assertEqual(saved_records[0]["session_id"],"MOCK-SESS-99")
    
   #========================================================
#EDGE CASES
#===========================================================
    def test_invalid_json_handling(self):
        """Ensures that corrupted JSON files fallback structures instead of breaking. """ 
        with open(self.test_kb_file,"w", encoding="utf-8") as f:
            f.write("{corrupt...}")
            fallback_data=self.storage.test_load_diagnosis_History()
            self.assertEqual(fallback_data,{"diseases":[]}) 

    def test_search_symptom_not_found_edge_case(self):
        # EDGE CASE: Verify searching for a symptom that does not exist  returns an empty list
        matches = self.storage.search_diseases_by_symptom("alien_hand_syndrome")
        self.assertIsInstance(matches,list)
        self.assertEqual(len(matches),0)

    def test_search_empty_or_witespace_query_edge_case(self):
        """EDGE CASE: Verify searching for pure spaces doesn't accidentally match or crash """
        # A bad input query full of empty spaces
        matches = self.storage.search_diseases_by_symptoms("   ")
        self.assertEqual(len(matches),0)

    def test_load_knowledge_base_file_missing_edge_case(self):
        """EDGE CASE: Verify that is the file is completely missing the system does not crash"""  
        # Force delete the file mid-execution to test missing file boundaries
        if os.path.exists(self.test_kb_file):
            os.remove(Self.test_kb_file)

            #Storage.py handles FileNotFoundError gratefully by returning a {"disease": []}
            fallback_data = self.storage.load_diagnosis_History()
            self.assertEqual(fallback_data, {"diseases": []})  

if__name__=="__main__":
    unittest.main()     