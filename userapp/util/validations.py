import re
import logging

import jsonschema
from jsonschema import validate

from userapp.util.constants import MINIMUM_NAME_LENGTH, MAXIMUM_NAME_LENGTH, MINIMUM_PASSWORD_LENGTH

LOGGER = logging.getLogger(__name__)


class Validator(object):

    @staticmethod
    def string_length_validation(val, minimum, maximum):
        LOGGER.debug("Validating length of string: {} with max: {} and min: {}".format(str(val), maximum, minimum))
        print("Validating length of string: {} with max: {} and min: {}".format(str(val), maximum, minimum))
        if minimum <= len(str(val)) <= maximum:
            return True
        LOGGER.error("Length validation fails")
        print("Length validation fails")
        return False

    @staticmethod
    def name_validation(val):
        LOGGER.debug("Validating name: {}".format(str(val)))
        print("Validating name: {}".format(str(val)))
        if Validator.string_length_validation(val, MINIMUM_NAME_LENGTH, MAXIMUM_NAME_LENGTH):
            return re.search('^[A-Za-z]{2,25}( [A-Za-z]{2,25})?', str(val))
        LOGGER.error("Name validation fails for name: {}".format(str(val)))
        print("Name validation fails for name: {}".format(str(val)))
        return False

    @staticmethod
    def email_validation(email):
        LOGGER.debug("Validating email: {}".format(str(email)))
        print("Validating email: {}".format(str(email)))
        regex = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"
        try:
            if not re.search(regex, email):
                LOGGER.error("Email validation fails for email: {}".format(str(email)))
                print("Email validation fails for email: {}".format(str(email)))
                return False
        except Exception as e:
            print(e)
        return True

    @staticmethod
    def password_validation(password):
        LOGGER.debug("Validating password:")
        print("Validating password")
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
        if not (d >= 1 and u >= 1 and l >= 1 and s >= 1):
            LOGGER.error("Password validation failed")
            print("Password validation failed")
            return False
        return True

    @staticmethod
    def validate_json(json_data, json_schema):
        try:
            LOGGER.debug("Validating form")
            print("Validating form")
            validate(instance=json_data, schema=json_schema)
        except jsonschema.exceptions.ValidationError as err:
            LOGGER.error("Form validation failed")
            print("Form validation failed")
            return False
        return True
