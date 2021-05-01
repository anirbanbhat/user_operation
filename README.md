# Release Notes

---
This is a simple user authentication back app written in Python flask and backed by MongoDB. This app has function of registering user with email id, name and password, list all registered users, login a registered user and update/delete a register user.

---
# API

---
This application have following api exposed:

| Function  | API | Method |
|-----------|-----|--------|
|Registered User|/app/useroperations/v1/users| POST |
|List Users|/app/useroperations/v1/users| GET |
|Login User|/app/useroperations/v1/users/user| POST |
|Update User|/app/useroperations/v1/users/<email>| PUT |
|Delete User|/app/useroperations/v1/users/<email>| DELETE |
|Health check|/|GET|
|Swagger API|/swagger|GET|

---
# Installing and Run Locally

Prerequisites
---
System should have python 3.7 or above, pip, setuptools, docker (if mongodb installed using docker container) installed in the system.

Installation Steps:
---
1. Install MongoDB
   - Start MongoDB
     - ```docker run -p 127.0.0.1:27017:27017 --name my-mongo -d mongo```
   - Get into the Mongo Container
     - ```docker exec -it user-db bash```
   - Get into the Mongo Shell
     - ```mongo```
   - Create database
     - ```use user-db```
   - Create collection
     - ```db.createCollection('users');```
2. Install user_operation app
   - Clone the repo and go to the user_operation directory from your terminal (or git bash/powershell)
   - Start virtual environment for python (Say the folder in venv)
     - source venv/bin/activate
   - Install the application
     - python3 setup.py
   - Run the application
     - python3 userapp/app.py

Congrats, your application is up and running. You can access the swagger api at 0.0.0.0/swagger URL

# Installing application in kubernetes cluster (minikube)

---
***Under Development***
