"""
    Written by ©Anirban Bhattacherji
    2021
"""

NAME_VALIDATION_ERR = 'Name should be 4 to 20 Characters and alpha-numeric value; '
EMAIL_VALIDATION_ERR = 'Please share proper email address; '
EMAIL_EXISTS = 'An account already exists with this email id'
EMAIL_DOES_NOT_EXIST = 'No account exists with this email id'
PASSWORD_VALIDATION_ERR = 'Password should 8 to 25 character and it should contain at least one upper case ' \
                          'one lower case one digit and and one special characters (@$#_); '
INTERNAL_ERR = 'Internal error occurred;'
INVALID_FORM_ERR = 'Invalid json form. Please check input data; '
INCORRECT_PASSWORD_ERR = 'Provided password in incorrect; '
HTTP_PARSE_ERR = 'Improper json format;'

SUCCESS_CREATED = 'User profile created successfully!'
SUCCESS_UPDATE = 'User profile updated successfully!'
SUCCESS_DELETE = 'User profile deleted successfully!'
SUCCESS_LOGIN = 'User logged in successfully at $time '

DATA_FIELD_NAME = 'name'
DATA_FIELD_EMAIL = 'email'
DATA_FIELD_PASSWORD = 'password'
DATA_LAST_LOGIN = 'lastLogIn'
DATE_FORMAT = "%d-%b-%Y (%H:%M:%S.%f)"

EMAIL_VALIDATION_REGEX = "^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"
NAME_VALIDATION_REGEX = "^[A-Za-z]{2,25}( [A-Za-z]{2,25})?"

MINIMUM_NAME_LENGTH = 4
MAXIMUM_NAME_LENGTH = 30
MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 20

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

OK = "OK"

DATABASE_COLLECTION = 'users'
DATABASE_NOT_AVAILABLE = "Database service is not available!"
