from setuptools import setup, find_packages

setup(
    name='user_operation',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['Flask==1.1.2', 'pymongo', 'bcrypt==3.1.4',
                      'jsonschema', 'Werkzeug==0.16.1', 'flask-swagger-ui==3.36.0']
)
