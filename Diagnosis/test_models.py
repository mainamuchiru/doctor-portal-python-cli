#This mainly checks on the file patient,Doctor and diagnosis
import unittest
from doctor import Doctor
from patient import Patient
from diagnosis import Diagnosis

class TestMedicalModels(unittest.TestCase):

    def setUp(self):
    """Set up standard mock objects matching your exact backend signature """
    # Match doctor.py constructor: name, doctor_id, password
    self.mock_doctor = Doctor(
        name = "Alice Mwenda",
        doctor_id = "D101",
        password = "docpass"
    )

    # Matc patient.py constructor: name,phone_number,date_of_birth
    self.mock_patient = Patient(
        name = "ann",
        phone_number="987674",
        date_of_birth = "1990-11-05"
    )
    #===========================================================
    # 1. HAPPY PATH TEST (Testing Expected Behavior)
    #===========================================================

    def test_doctor_initialization(self):
        """HAPPY PATH: Verifies doctor attributes strip correctly and authentication"""
    self.assertEqual(self.mock_doctor.name, "ann")
    self.assertEqual(self.mock_doctor.doctor_id, "D101")
    # Valid password input must evaluate to true
    self.assertTrue(self.mock_doctor.check_password("docpass"))

    def test_patient_py_path(self):
        """HAPPY PATH: Verify unique patient ID auto-generate perfectly"""
        self.assertEqual(self.mock_patient.name, "ann")
        self.assertEqual(self.mock_patient.phone_number, "987674")
        #Ensure ID GENERATION FROM INHERITANCE WORKS
        SELF.assertIsNotNone(self.mock_patient.patient_id)
        self.assertTrue(len(self.mock_patient.patient_id)str)

    def test_diagnosis_assignment_happy_path(self):
        """HAPPY PATH: Verify symptoms and conditions update through properties"""
        diag = Diagnosis(
            session_id="4b93e907-2d1d-4dd8-9e27-437c0ec540e7",
            patient_id=self.mock_patient.patient_id,
            doctor_id= self.mock_doctor.doctor_id
        )
        #Using my valid setter properties
        diag.disease="Malaria"
        self.assertEqual(diag.disease, "Malaria")
#=================================================================       
#EDGE CASES
#==================================================================
    def test_doctor_failed_authentication_edge_case(self):
        """EDGE CASE: Verify wrong passwords or empty authentication"""
        # Any wrong password it should return a False
        self.assertFalse(self.mock_doctor.check_password("wrong_password"))
        self.assertFalse(self.mock_doctor.check_password(""))
   
    def test_patient_whitespace_cleanup_edge_case(self):
        """EDGE CASE: Verify constructor cleans meassy spacing using the .strip"""
        messy_patient= Patient(
            name=" ann ",
            phone_number="987674",
            date_of_birth="1990-11-05"
        )    

    #My models contain .strips() values are equal to the cleaned versions
        self.assertEqual(messy_patient.name,"ann")
        self.assertEqual(messy_patient.phone_number,"987674")

    def test_diagnosis_empty_validation_edge_case(self):
        """ EDGE CASE: Verify blank or empty inputs trigger your custom" ValueError guard"""
        diag = Diagnosis(
            session_id= "4b93e907-2d1d-4dd8-9e27-437c0ec540e7"
            patient_id=self.mock_patient.patient_id,
            doctor_id= self.mock_doctor.doctor_id
        )

    #Test 1: Setting an empty text string must raise your VlaueError
    with self.assertRaises(ValueError):
        diag.disease=""
    with self.assertRaises(ValueError):
        diag.disease="       "

        if __name__ =="__main__":
            unittest.main()        