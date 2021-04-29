from flask import request, jsonify, Blueprint, current_app

from userapp.util import constants
from userapp.util.validations import Validator
from userapp.business import user_service

REQUEST_API = Blueprint('request_api', __name__)


@REQUEST_API.route("/app/useroperations/v1/users", methods=[constants.POST])
def create_user():
    """Creates new user"""
    current_app.logger.debug("POST: Creates new user")
    data = request.get_json(force=True)
    is_valid, msg, err_code, updated_data = user_service.validate_registration(data)
    if not is_valid:
        return jsonify(error=msg), err_code
    if not user_service.insert_data(updated_data):
        current_app.logger.error("Exception occurred while updating the database")
        return jsonify(error=constants.INTERNAL_ERR), 500
    current_app.logger.debug("User Registered successfully")
    return jsonify(message=constants.SUCCESS_CREATED), 201


@REQUEST_API.route("/app/useroperations/v1/users", methods=[constants.GET])
def list_users():
    """Returns all users"""
    current_app.logger.debug("GET: List all new user")
    err, response = user_service.get_all()
    if err:
        return jsonify(error=constants.INTERNAL_ERR), 500
    return jsonify(response), 200


@REQUEST_API.route("/app/useroperations/v1/users/user/", methods=[constants.POST])
def login_user():
    """Returns user based on email/password"""
    current_app.logger.debug("POST: Login with email and password")
    data = request.get_json(force=True)
    is_valid, msg, err_code = user_service.validate_login(data)
    if not is_valid:
        return jsonify(error=msg), err_code
    err, response, code = user_service.update_login(data)
    if err:
        return jsonify(error=response), code
    return jsonify(message=response), code


@REQUEST_API.route("/app/useroperations/v1/users/<string:email>", methods=[constants.PUT])
def update_user(email):
    """Updates user based on email"""
    current_app.logger.debug("PUT: Update name or password")
    data = request.get_json(force=True)
    is_valid, msg, err_code, update_query = user_service.validate_updation(data, email)
    if not is_valid:
        return jsonify(error=msg), err_code
    if not user_service.update_data(email, update_query):
        return jsonify(error=constants.INTERNAL_ERR), 500
    return jsonify(message=constants.SUCCESS_UPDATE), 204


@REQUEST_API.route("/app/useroperations/v1/users/<string:email>", methods=[constants.DELETE])
def delete_user(email):
    """Deletes user based on email"""
    current_app.logger.debug("DELETE: Delete user detail")
    if not Validator.email_validation(email):
        return jsonify(error=constants.EMAIL_VALIDATION_ERR), 400
    if not user_service.email_exist(email):
        return jsonify(error=constants.EMAIL_DOES_NOT_EXIST), 404
    if not user_service.delete_user(email):
        return jsonify(error=constants.INTERNAL_ERR), 500
    return jsonify(message=constants.SUCCESS_DELETE), 204
