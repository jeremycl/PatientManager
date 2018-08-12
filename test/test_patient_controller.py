import unittest
from common.config import connex_app, db
from models.db_model import Patient, PatientAttributes
from datetime import date


class PatientModelCase(unittest.TestCase):
    connex_app.app.config['TESTING'] = True
    connex_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    connex_app.add_api('swagger.yml', arguments={'title': 'User API'})

    def setUp(self):
        db.create_all()
        self.app = connex_app.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Verify patient_get returns 200 response and contains no data (0 patients, page 1 for both links)
    def test_patient_get_200(self):
        response = self.app.get('/v1/patients')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['data'].__len__(), 0)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=1'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=1'))

    # Verify patient_get returns 200 response with data (2 patients, page 1 for both links)
    def test_patient_get_200_data(self):
        PATIENTS = [
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob@robert.com'},
            {'birthdate': date(1950, 2, 5), 'sex': 'F', 'last_name': 'Something', 'first_name': 'Linda',
             'email': 'linda@gmail.com'}
        ]

        self.populate_patients(PATIENTS)

        response = self.app.get('/v1/patients')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['data'].__len__(), 2)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=1'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=1'))

    # Verify patient_get returns 200 response with data (11 patients, 10 items on page 1, 1 item on page 2, 0 item on page 3)
    def test_patient_get_200_data_large(self):
        PATIENTS = [
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob1@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob2@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob3@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob4@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob5@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob6@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob7@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob8@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob9@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob10@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob11@robert.com'},
        ]

        self.populate_patients(PATIENTS)

        response = self.app.get('/v1/patients')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['data'].__len__(), 10)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=1'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=2'))

        response = self.app.get('/v1/patients?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'].__len__(), 1)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=2'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=2'))

        # Page with no data should return no data and link back to page 1
        response = self.app.get('/v1/patients?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'].__len__(), 0)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=3'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=1'))

        # Invalid page (less than 1) returns page 1
        response = self.app.get('/v1/patients?page=-1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'].__len__(), 10)
        self.assertTrue(str(response.json['links']['self']).__contains__('page=1'))
        self.assertTrue(str(response.json['links']['next']).__contains__('page=2'))

    # Verify patient_id_get returns 404 with empty db
    def test_patient_id_get_404(self):
        response = self.app.get('/v1/patients/1')
        self.assertEqual(response.status_code, 404)

    # Verify patient_id_get with data (2 patients)
    def test_patient_id_get_200(self):
        PATIENTS = [
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob1@robert.com'},
            {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob',
             'email': 'bob2@robert.com'}
        ]

        self.populate_patients(PATIENTS)

        response = self.app.get('/v1/patients/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__len__(),1)
        self.assertEqual(response.json['attributes']['email'],'bob1@robert.com')

        response = self.app.get('/v1/patients/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__len__(), 1)
        self.assertEqual(response.json['attributes']['email'], 'bob2@robert.com')

        # Invalid patient ID
        response = self.app.get('/v1/patients/3')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['errors'].__len__(), 1)

    # Verify patients_post returns 400 when passing erroneous values
    def test_patients_post_400(self):
        # Invalid birthdate, email, firstname, lastname and sex. Returns 5 errors and 400 status
        response = self.app.post('/v1/patients', json={
            "data": {
                "attributes": {
                    "birthdate": "20181-08-12",
                    "email": "testtest.com",
                    "first_name": "123",
                    "last_name": "345",
                    "sex": "MM"
                }
            }
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['errors'].__len__(),5)

        # Invalid birthdate. Returns 1 error and 400 status
        response = self.app.post('/v1/patients', json={
            "data": {
                "attributes": {
                    "birthdate": "20181-08-12",
                    "email": "test@test.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "sex": "M"
                }
            }
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['errors'].__len__(), 1)

        # Validate nothing was added to db
        response = self.app.get('/v1/patients')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['data'].__len__(), 0)

    # Verify patients_post returns 200 when passing valid values
    def test_patients_post_200(self):
        # Valid data, returns status 200 and patient data
        response = self.app.post('/v1/patients', json={
            "data": {
                "attributes": {
                    "birthdate": "2018-08-12",
                    "email": "test@test.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "sex": "M"
                }
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__len__(), 1)
        self.assertEqual(response.json['attributes']['email'], 'test@test.com')

        # Validate 1 patient was added to db
        response = self.app.get('/v1/patients')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data'].__len__(), 1)
        self.assertEqual(response.json['data'][0]['attributes']['email'], 'test@test.com')

    # Verify patients_post returns 409 when adding patient with already existing email
    def test_patients_post_409(self):
        # Valid data, returns status 200 and patient data
        response = self.app.post('/v1/patients', json={
            "data": {
                "attributes": {
                    "birthdate": "2018-08-12",
                    "email": "test@test.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "sex": "M"
                }
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.__len__(), 1)
        self.assertEqual(response.json['attributes']['email'], 'test@test.com')

        # Add other patient with same email, returns 409 and error
        response = self.app.post('/v1/patients', json={
            "data": {
                "attributes": {
                    "birthdate": "2016-01-01",
                    "email": "test@test.com",
                    "first_name": "TestTwo",
                    "last_name": "UserTwo",
                    "sex": "M"
                }
            }
        })
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['errors'].__len__(), 1)

    # Populates patients to db
    def populate_patients(self,PATIENTS):
        for patient in PATIENTS:
            p = Patient()
            pAttributes = PatientAttributes(email=patient.get('email'), first_name=patient.get('first_name'),
                                            last_name=patient.get('last_name'), birthdate=patient.get('birthdate'),
                                            sex=patient.get('sex'), patient=p)
            db.session.add(pAttributes)
        db.session.commit()


    if __name__ == '__main__':
            unittest.main()
