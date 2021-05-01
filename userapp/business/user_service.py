"""
    Written by ©Anirban Bhattacherji
    2021
"""

from datetime import datetime

import bcrypt
from string import Template
from flask import current_app, json

from userapp.util import schema, constants
from userapp.util.exception import CustomErr
from userapp.util.validations import Validator
from userapp.db_access.database import Database
from userapp.db_access import db_query


def validate_registration(data):
    current_app.logger.debug("Validating registration data")
    Validator.validate_json(data, schema.register_schema)
    email = data[constants.DATA_FIELD_EMAIL]
    Validator.email_validation(email)
    try:
        exists, err = email_exist(email)
        if err:
            return False, err, 500, None
        if exists:
            return False, constants.EMAIL_EXISTS, 400, None
    except Exception as e:
        return False, constants.INTERNAL_ERR, 500, None
    name = data[constants.DATA_FIELD_NAME]
    Validator.name_validation(name)
    password = data[constants.DATA_FIELD_PASSWORD]
    Validator.password_validation(password)
    date = datetime.now().strftime(constants.DATE_FORMAT)
    current_app.logger.debug("Hashing the password before storing")
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    user_data = {
        constants.DATA_FIELD_NAME: name,
        constants.DATA_FIELD_EMAIL: email,
        constants.DATA_FIELD_PASSWORD: hashed_password,
        constants.DATA_LAST_LOGIN: date
    }
    return user_data


def validate_updation(data, email):
    current_app.logger.debug("Validating update data for email: {}".format(email))
    Validator.email_validation(email)
    if not email_exist(email):
        raise CustomErr(constants.EMAIL_DOES_NOT_EXIST, 400)
    Validator.validate_json(data, schema.update_schema)
    new_values = {}
    if data[constants.DATA_FIELD_NAME]:
        name = data[constants.DATA_FIELD_NAME]
        Validator.name_validation(name)
        new_values[constants.DATA_FIELD_NAME] = name
    if data[constants.DATA_FIELD_PASSWORD]:
        password = data[constants.DATA_FIELD_PASSWORD]
        Validator.password_validation(password)
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        new_values[constants.DATA_FIELD_PASSWORD] = hashed_password
    date = datetime.now().strftime(constants.DATE_FORMAT)
    new_values[constants.DATA_LAST_LOGIN] = date
    return {"$set": new_values}


def validate_login(data):
    current_app.logger.debug("Validating login data: {}".format(str(data)))
    Validator.validate_json(data, schema.login_schema)
    email = data[constants.DATA_FIELD_EMAIL]
    Validator.email_validation(email)
    if not email_exist(email):
        raise CustomErr(constants.EMAIL_DOES_NOT_EXIST, 400)


def insert_data(data):
    current_app.logger.debug("Inserting registration data")
    Database.insert(constants.DATABASE_COLLECTION, data)


def update_data(email, update_query):
    current_app.logger.debug("Updating registration data for email: {}".format(email))
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL, value=email))
    if not type(update_query) is dict:
        update_query = json.loads(update_query)
    current_app.logger.debug("update_query: {}".format(str(update_query)))
    Database.update(constants.DATABASE_COLLECTION, filter_query, update_query)


def update_login(data):
    current_app.logger.debug("Logging in for the registered user")
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL,
                                                      value=data[constants.DATA_FIELD_EMAIL]))
    date = datetime.now().strftime(constants.DATE_FORMAT)
    update_query = '{ "$set": { "lastLogIn": "' + date + '" }}'
    update_query = json.loads(update_query)
    if verify_password(filter_query, data[constants.DATA_FIELD_PASSWORD]):
        Database.update(constants.DATABASE_COLLECTION, filter_query, update_query)
        return Template(constants.SUCCESS_LOGIN).substitute(time=date)
    else:
        raise CustomErr(constants.INCORRECT_PASSWORD_ERR, 400)


def delete_user(email):
    current_app.logger.debug("Deleting for the registered user profile")
    Validator.email_validation(email)
    if not email_exist(email):
        raise CustomErr(constants.EMAIL_DOES_NOT_EXIST)
    filter_query = Template(db_query.DATABASE_FILTER_QUERY)
    filter_query = json.loads(filter_query.substitute(field=constants.DATA_FIELD_EMAIL, value=email))
    Database.delete(constants.DATABASE_COLLECTION, filter_query)


def get_all():
    current_app.logger.debug("Retrieving all users")
    filter_query = json.loads(db_query.DATABASE_GET_ALL_FILTER_QUERY)
    projection_query = json.loads(db_query.DATABASE_GET_ALL_PROJECTION_QUERY)
    cursor = Database.get_all(constants.DATABASE_COLLECTION, filter_query, projection_query)
    list_cur = list(cursor)
    list_cur


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


def health_check():
    Database.health()
