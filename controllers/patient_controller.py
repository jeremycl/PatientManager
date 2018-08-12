import connexion
from common.config import db
from models.db_model import Patient, PatientAttributes
from models.http_error import HttpError
from models.pagination import Pagination
from models.errors import MultipleErrors, InputError, DuplicateError
from flask import jsonify, request
from datetime import datetime


def patient_get():
    try:
        # Retrieve current page from request args. Set to 1 if not specified.
        currPage = request.args.get('page', default=1, type=int)

        if currPage < 1:
            currPage = 1

        # Retrieve all Patient IDs in DB
        patientList = Patient.query.order_by(Patient.id).all()
        patientIDs = [i.id for i in patientList]

        # Build sublist of patient IDs for the specified page
        endIndex = currPage * 10
        startIndex = endIndex - 10
        pagePatientList = patientIDs[startIndex:endIndex]

        # Retrieve all PatientAttributes of matching Patient IDs
        patientAttr = PatientAttributes.query.filter(PatientAttributes.patient_id.in_(pagePatientList)).all()

        # Build links for pages
        nextPage = currPage

        # If current page is empty, next and current page equal to 1
        if pagePatientList.__len__() <= 0:
            nextPage = 1

        # If not enough content for a next page, next page = current page
        elif endIndex >= patientIDs.__len__():
            nextPage = currPage

        else:
            nextPage = currPage + 1

        links = Pagination(_self='./patients?page=' + str(currPage),_next='./patients?page=' + str(nextPage))

        return jsonify(data=[i.serialize for i in patientAttr], links=links.serialize)

    except:
        return jsonify(data=[], links={})


def patient_id_get(id):
    try:
        # Verify if Patient ID exists in the Patient table
        patient = Patient.query.filter_by(id=id).first()

        # Patient ID does not exist, return 404 error message
        if patient is None:
            raise ValueError("No patient with ID {pID} has been found".format(pID=id))

        patientAttr = PatientAttributes.query.filter_by(patient_id=id).first()

        return jsonify(patientAttr.serialize)

    except Exception as e:
        # Generate HttpError and return 404
        error = HttpError(id=1, status=404, title='Error', detail=e.args[0], source=e)

        return jsonify(errors=[error.serialize]), 404


def patients_post(body=None):
    try:
        if connexion.request.is_json:
            body = connexion.request.get_json()
            attributes = body['data']['attributes']
            email = attributes.get('email').strip()
            fname = attributes.get('first_name').strip()
            lname = attributes.get('last_name').strip()
            birthdate = attributes.get('birthdate')
            sex = attributes.get('sex').upper().strip()

            # Validate all inputs
            errorList = validate_inputs(email, fname, lname, birthdate, sex)
            if errorList.__len__() > 0:
                raise MultipleErrors(errors=errorList)

            # Verify for any email duplicates
            alreadyExists = PatientAttributes.query \
                .filter(PatientAttributes.email == email)\
                .one_or_none()

            if alreadyExists is None:
                # Create new patient and patientattributes records
                p = Patient()

                birthdate_date = datetime.strptime(birthdate, '%Y-%m-%d').date()
                pAttributes = PatientAttributes(email=email, first_name=fname,
                                                last_name=lname, birthdate=birthdate_date,
                                                sex=sex, patient=p)

                db.session.add(pAttributes)
                db.session.commit()

                return jsonify(pAttributes.serialize)

            else:
                # Record with same email already exists, raise error
                raise DuplicateError(expression=email, message='Email already exists')

    except MultipleErrors as e:
        httpErrors = []
        i=1
        for err in e.errors:
            httpErrors.append(HttpError(id=i, status=400, title='Input Error', detail=err.message, source=err.serialize))
            i+=1

        return jsonify(errors=[i.serialize for i in httpErrors]),400

    except InputError as e:
        # Generate HttpError and return 409
        error = HttpError(id=1, status=400, title='Input Error', detail=e.message, source=e.serialize)
        return jsonify(errors=[error.serialize]), 400

    except DuplicateError as e:
        error = HttpError(id=1, status=409, title='Duplicate Error', detail=e.message, source=e.serialize)
        return jsonify(errors=[error.serialize]), 409

    except Exception as e:
        # Generate HttpError and return 400
        error = HttpError(id=1, status=400, title='Error', source=e)

        return jsonify(errors=[error.serialize]), 400


# Verifies inputs for any input errors
def validate_inputs(email, fname, lname, birthdate, sex):
    errors = []

    # Verify proper email format
    if ('@' not in email) or ('.' not in email):
        errors.append(InputError(expression=email, message='Invalid email format'))

    # Verify valid characters in first name or last name
    if not valid_alpha_input(fname):
        errors.append(InputError(expression=fname, message='Invalid first name. Alphabet characters only'))

    if not valid_alpha_input(lname):
        errors.append(InputError(expression=lname, message='Invalid last name. Alphabet characters only'))

    # Verify proper date format
    try:
        birthdate_date = datetime.strptime(birthdate, '%Y-%m-%d').date()
    except:
        errors.append(InputError(expression=birthdate,
                         message='Invalid birthdate. Please enter in format YYYY-MM-DD'))

    # Verify proper value for sex
    if (sex != 'M') and (sex != 'F'):
        errors.append(InputError(expression=sex, message="Invalid Sex. Please enter 'M' or 'F'"))

    return errors


# Verifies string for only alphabet characters or space
def valid_alpha_input(input):
    for character in input:
        if not character.isalpha() and character != ' ':
            return False
    return True

