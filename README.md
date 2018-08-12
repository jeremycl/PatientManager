# Jeremy's Patient Manager

## Instructions

Go to containing folder

```
# wherever you placed the folder
cd /Users/jeremy/Downloads/PatientManager/
```

Create venv (was built using Python 3.7)

```
virtualenv venv
```

Activate venv, install requirements then deactivate venv

```
source venv/bin/activate
pip install -r requirements.txt 
deactivate
```

Using python from the venv, you can now run the following:

```
# To run the flask server
# Swagger UI will be available at the URL http://{server_url}/v1/ui/ 
# i.e. http://0.0.0.0:5000/v1/ui/
/Users/jeremy/Downloads/PatientManager/venv/bin/python server.py 

# To build or rebuild a fresh patient.db that contains 2 default patients
/Users/jeremy/Downloads/PatientManager/venv/bin/python build_database.py 

# To run the tests
cd /Users/jeremy/Downloads/PatientManager
/Users/jeremy/Downloads/PatientManager/venv/bin/python -m unittest /Users/jeremy/Downloads/PatientManager/test/test_patient_controller.py
```
