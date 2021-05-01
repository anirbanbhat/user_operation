"""
    Written by ©Anirban Bhattacherji
    2021
"""

import logging.config
import os
from flask import Flask

from userapp import settings
from userapp.db_access.database import Database
from flask_swagger_ui import get_swaggerui_blueprint

from userapp.routes import user_endpoints

app = Flask(__name__)
logger_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logger_conf_path)
LOGGER = logging.getLogger(__name__)

"""Swagger Configuration"""
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "user_operation"
    }
)


def initialize_app(flask_app):
    """Initializing flask app"""
    flask_app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    flask_app.register_blueprint(user_endpoints.REQUEST_API)
    Database.initialize(os.environ.get('MONGODB_HOST', settings.MONGODB_HOST),
                        os.environ.get('MONGODB_PORT', settings.MONGODB_PORT),
                        os.environ.get('MONGODB_DATABASE', settings.MONGODB_DATABASE))


if __name__ == "__main__":
    initialize_app(app)
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', 5000),
            debug=os.environ.get('FLASK_DEBUG', settings.FLASK_DEBUG))
