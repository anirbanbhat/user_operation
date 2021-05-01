"""
    Written by ©Anirban Bhattacherji
    2021
"""

import re
import logging

import jsonschema
from jsonschema import validate
from flask import current_app

from userapp.util import constants
from userapp.util.constants import MINIMUM_NAME_LENGTH, MAXIMUM_NAME_LENGTH, MINIMUM_PASSWORD_LENGTH
from userapp.util.exception import CustomErr

LOGGER = logging.getLogger(__name__)


class Validator(object):

    @staticmethod
    def string_length_validation(val, minimum, maximum):
        current_app.logger.debug("Validating length of string: {} with max: {} and min: {}"
                                 .format(str(val), maximum, minimum))
        if minimum <= len(str(val)) <= maximum:
            return True
        current_app.logger.error("Length validation fails")
        print("Length validation fails")
        return False

    @staticmethod
    def name_validation(val):
        current_app.logger.debug("Validating name: {}".format(str(val)))
        if not Validator.string_length_validation(val, MINIMUM_NAME_LENGTH, MAXIMUM_NAME_LENGTH) \
                and not re.search(constants.NAME_VALIDATION_REGEX, str(val)):
            current_app.logger.error("Name validation fails for name: {}".format(str(val)))
            raise CustomErr(constants.NAME_VALIDATION_ERR, 400)

    @staticmethod
    def email_validation(email):
        current_app.logger.debug("Validating email: {}".format(str(email)))
        if not re.search(constants.EMAIL_VALIDATION_REGEX, email):
            current_app.logger.error("Email validation fails for email: {}".format(str(email)))
            raise CustomErr(constants.EMAIL_VALIDATION_ERR, 400)

    @staticmethod
    def password_validation(password):
        current_app.logger.debug("Validating password:")
        d, l, u, s = 0, 0, 0, 0
        if Validator.string_length_validation(password, MINIMUM_PASSWORD_LENGTH, MAXIMUM_NAME_LENGTH):
            for char in password:
                if char.isdigit():
                    d += 1
                if char.isupper():
                    u += 1
                if char.islower():
                    l += 1
                if char == '@' or char == '$' or char == '_' or char == '#':
                    s += 1
        if d >= 1 and u >= 1 and l >= 1 and s >= 1:
            return
        current_app.logger.error("Password validation failed")
        raise CustomErr(constants.PASSWORD_VALIDATION_ERR, 400)

    @staticmethod
    def validate_json(json_data, json_schema):
        try:
            current_app.logger.debug("Validating form")
            validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError as err:
            current_app.logger.error("Form validation failed")
            raise CustomErr(constants.INVALID_FORM_ERR, 400)
        '''except Exception as err:
            current_app.logger.error("Form validation failed")
            raise CustomErr(constants.INVALID_FORM_ERR, 400)'''
