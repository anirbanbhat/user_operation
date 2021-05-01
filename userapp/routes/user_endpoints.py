from http.client import HTTPException

from flask import request, jsonify, Blueprint, current_app

from userapp.util import constants
from userapp.util.exception import CustomErr
from userapp.business import user_service

REQUEST_API = Blueprint('request_api', __name__)


@REQUEST_API.route("/app/useroperations/v1/users", methods=[constants.POST])
def create_user():
    """Creates new user"""
    current_app.logger.debug("POST: Creates new user")
    try:
        data = request.get_json(force=True)
        updated_data = user_service.validate_registration(data)
        user_service.insert_data(updated_data)
        current_app.logger.debug("User Registered successfully")
        return jsonify(message=constants.SUCCESS_CREATED), 201
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code
    except Exception as err:
        current_app.logger.error(err)
        return jsonify(error=constants.INTERNAL_ERR), 500


@REQUEST_API.route("/app/useroperations/v1/users", methods=[constants.GET])
def list_users():
    """Returns all users"""
    current_app.logger.debug("GET: List all new user")
    try:
        response = user_service.get_all()
        return jsonify(response), 200
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code
    except Exception as err:
        current_app.logger.error(err)
        return jsonify(error=constants.INTERNAL_ERR), 500


@REQUEST_API.route("/app/useroperations/v1/users/user/", methods=[constants.POST])
def login_user():
    """Returns user based on email/password"""
    current_app.logger.debug("POST: Login with email and password")
    try:
        data = request.get_json(force=True)
        user_service.validate_login(data)
        response = user_service.update_login(data)
        return jsonify(message=response), 201
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code
    except HTTPException as eh:
        current_app.logger.error(eh)
        return jsonify(error=constants.HTTP_PARSE_ERR), 400
    except Exception as err:
        current_app.logger.error(err)
        return jsonify(error=constants.INTERNAL_ERR), 500


@REQUEST_API.route("/app/useroperations/v1/users/<string:email>", methods=[constants.PUT])
def update_user(email):
    """Updates user based on email"""
    current_app.logger.debug("PUT: Update name or password")
    try:
        data = request.get_json(force=True)
        update_query = user_service.validate_updation(data, email)
        user_service.update_data(email, update_query)
        return jsonify(message=constants.SUCCESS_UPDATE), 204
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code
    except Exception as err:
        current_app.logger.error(err)
        return jsonify(error=constants.INTERNAL_ERR), 500


@REQUEST_API.route("/app/useroperations/v1/users/<string:email>", methods=[constants.DELETE])
def delete_user(email):
    """Deletes user based on email"""
    current_app.logger.debug("DELETE: Delete user detail")
    try:
        user_service.delete_user(email)
        return jsonify(message=constants.SUCCESS_DELETE), 204
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code
    except Exception as err:
        current_app.logger.error(err)
        return jsonify(error=constants.INTERNAL_ERR), 500


@REQUEST_API.route("/", methods=[constants.GET])
def health_check():
    """Health check API"""
    current_app.logger.debug("GET: Health check API. Service is running okay")
    try:
        user_service.health_check()
        return jsonify(message=constants.OK), 200
    except CustomErr as e:
        current_app.logger.error(e)
        return jsonify(error=e.message), e.code

