from datetime import datetime

import bcrypt
from string import Template
from flask import current_app, json

from userapp.util import schema, constants
from userapp.util.validations import Validator
from userapp.db_access.database import Database
from userapp.db_access import db_query


def validate_registration(data):
    current_app.logger.debug("Validating registration data: {}".format(str(data)))
    valid_form = Validator.validate_json(data, schema.register_schema)
    msg = ""
    if not valid_form:
        msg = constants.INVALID_FORM_ERR
        return valid_form, msg, 400, None
    email = data[constants.DATA_FIELD_EMAIL]
    if not Validator.email_validation(email):
        valid_form = False
        msg = msg + constants.EMAIL_VALIDATION_ERR
    if valid_form:
        try:
            if email_exist(email):
                return False, constants.EMAIL_EXISTS, 400, None
        except Exception as e:
            return False, constants.INTERNAL_ERR, 500, None
    name = data[constants.DATA_FIELD_NAME]
    if not Validator.name_validation(name):
        valid_form = False
        msg = msg + constants.NAME_VALIDATION_ERR
    password = data[constants.DATA_FIELD_PASSWORD]
    if not Validator.password_validation(password):
        valid_form = False
        msg = msg + constants.PASSWORD_VALIDATION_ERR
    if not valid_form:
        return valid_form, msg, 400, None
    date = datetime.now().strftime(constants.DATE_FORMAT)
    current_app.logger.debug("Hashing the password before storing")
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    user_data = {
        constants.DATA_FIELD_NAME: name,
        constants.DATA_FIELD_EMAIL: email,
        constants.DATA_FIELD_PASSWORD: hashed_password,
        constants.DATA_LAST_LOGIN: date
    }
    return valid_form, None, None, user_data


def validate_updation(data, email):
    current_app.logger.debug("Validating update data for email: {}".format(email))
    email_exists = email_exist(email)
    if not email_exists:
        return False, constants.EMAIL_DOES_NOT_EXIST, 404, None
    valid_form = Validator.validate_json(data, schema.update_schema)
    msg = ""
    new_values = {}
    if data[constants.DATA_FIELD_NAME]:
        name = data[constants.DATA_FIELD_NAME]
        if not Validator.name_validation(name):
            valid_form = False
            msg = msg + constants.NAME_VALIDATION_ERR
        else:
            new_values[constants.DATA_FIELD_NAME] = name
    if data[constants.DATA_FIELD_PASSWORD]:
        password = data[constants.DATA_FIELD_PASSWORD]
        if not Validator.password_validation(password):
            valid_form = False
            msg = msg + constants.PASSWORD_VALIDATION_ERR
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            new_values[constants.DATA_FIELD_PASSWORD] = hashed_password
    if not valid_form:
        return valid_form, msg, 400, None
    date = datetime.now().strftime(constants.DATE_FORMAT)
    new_values[constants.DATA_LAST_LOGIN] = date
    new_values = {"$set": new_values}
    return valid_form, constants.SUCCESS_CREATED, 204, new_values


def validate_login(data):
    current_app.logger.debug("Validating login data: {}".format(str(data)))
    valid_form = Validator.validate_json(data, schema.login_schema)
    msg = ""
    if not valid_form:
        msg = constants.INVALID_FORM_ERR
        return valid_form, msg, 400, None
    email = data[constants.DATA_FIELD_EMAIL]
    if not Validator.email_validation(email):
        valid_form = False
        msg = msg + constants.EMAIL_VALIDATION_ERR
    if valid_form:
        try:
            if not email_exist(email):
                return False, constants.EMAIL_EXISTS, 404
        except Exception as e:
            return False, constants.INTERNAL_ERR, 500
    if not valid_form:
        return valid_form, msg, 400
    return valid_form, None, None


def insert_data(data):
    current_app.logger.debug("Inserting registration data")
    return Database.insert(constants.DATABASE_COLLECTION, data)


def update_data(email, update_query):
    current_app.logger.debug("Updating registration data for email: {}".format(email))
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL, value=email))
    if not type(update_query) is dict:
        update_query = json.loads(update_query)
    current_app.logger.debug("update_query: {}".format(str(update_query)))
    return Database.update(constants.DATABASE_COLLECTION, filter_query, update_query)


def update_login(data):
    current_app.logger.debug("Logging in for the registered user")
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL,
                                                      value=data[constants.DATA_FIELD_EMAIL]))
    date = datetime.now().strftime(constants.DATE_FORMAT)
    update_query = '{ "$set": { "lastLogIn": "' + date + '" }}'
    update_query = json.loads(update_query)
    try:
        if verify_password(filter_query, data[constants.DATA_FIELD_PASSWORD]):
            Database.update(constants.DATABASE_COLLECTION, filter_query, update_query)
        else:
            return True, constants.INCORRECT_PASSWORD_ERR, 400
        login_message = Template(constants.SUCCESS_LOGIN)
        login_message = login_message.substitute(time=date)
        return False, login_message, 200
    except Exception as e:
        return True, constants.INTERNAL_ERR, 500


def delete_user(email):
    current_app.logger.debug("Deleting for the registered user profile")
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL, value=email))
    return Database.delete(constants.DATABASE_COLLECTION, filter_query)


def get_all():
    current_app.logger.debug("Retrieving all users")
    try:
        filter_query = json.loads(db_query.DATABASE_GET_ALL_FILTER_QUERY)
        projection_query = json.loads(db_query.DATABASE_GET_ALL_PROJECTION_QUERY)
        cursor = Database.get_all(constants.DATABASE_COLLECTION, filter_query, projection_query)
        list_cur = list(cursor)
        return False, list_cur
    except Exception as e:
        return True, constants.INTERNAL_ERR


def email_exist(email):
    current_app.logger.debug("Verifying if email: {} already exists".format(email))
    email_query = Template(db_query.DATABASE_FILTER_QUERY)
    email_query = json.loads(email_query.substitute(field=constants.DATA_FIELD_EMAIL, value=email))
    current_app.logger.debug("email_query: {}".format(str(email_query)))
    exists = False
    cursor = Database.get(constants.DATABASE_COLLECTION, email_query)
    list_cur = list(cursor)
    current_app.logger.debug("existing_data: {}".format(str(list_cur)))
    if bool(list_cur):
        current_app.logger.debug("Email: {} already exists".format(email))
        exists = True
    return exists


def verify_password(filter_query, password):
    hash_password = Database.get(constants.DATABASE_COLLECTION, filter_query)[0][constants.DATA_FIELD_PASSWORD]
    return bcrypt.hashpw(password.encode('utf8'), hash_password) == hash_password
