from setuptools import setup, find_packages


setup(
    name='user_operation',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['Flask', 'Flask-PyMongo', 'pymongo', 'bcrypt', 'jsonschema', 'flask-restplus==0.9.2',
                      'Werkzeug==0.16.1', 'flask-swagger-ui==3.20.9', 'flask_cors==3.0.7']
)