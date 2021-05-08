"""
    Written by ©Anirban Bhattacherji
    2021
"""

from pymongo import MongoClient, errors, ASCENDING
from flask import current_app
from userapp.util.exception import CustomErr

from userapp.util import constants


class Database(object):
    DATABASE = None
    client = None

    @staticmethod
    def initialize(host, port, db):
        """
        As Guide says "In PyMongo 3, the MongoClient constructor no longer blocks while connecting to the
        server or servers, and it no longer raises ConnectionFailure if they are unavailable, nor
        ConfigurationError if the user’s credentials are wrong. Instead, the constructor returns immediately
        and launches the connection process on background threads. The connect option is added to control
        whether these threads are started immediately, or when the client is first used."

        Hence, we will use atabase.client.server_info() for temporary solution
        ref: https://stackoverflow.com/questions/34243707/pymongo-3-2-connectionfailure-not-working
        """
        try:
            Database.client = MongoClient(host=host, port=int(port), serverSelectionTimeoutMS=2000)
            Database.DATABASE = Database.client[db]
        except errors.ServerSelectionTimeoutError as err:
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)
        except AttributeError as err:
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)


    @staticmethod
    def insert(collection, data):
        current_app.logger.debug("Inserting to the collection: {}".format(collection))
        try:
            Database.client.server_info()
            Database.DATABASE[collection].insert(data)
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while inserting to the collection: {}: {}"
                                     .format(collection, str(err)))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def get(collection, query):
        current_app.logger.debug("Retrieving from the collection: {}".format(collection))
        try:
            Database.client.server_info()
            return Database.DATABASE[collection].find(query)
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while retrieving from the collection: {}: {}"
                                     .format(collection, str(err)))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def get_all(collection, filter_query, projection_query, skips, page_size, sort_by):
        current_app.logger.debug("Listing all and projecting from the collection: {}".format(collection))
        try:
            Database.client.server_info()
            return Database.DATABASE[collection]\
                .find(filter_query, projection_query)\
                .sort("abc", ASCENDING)\
                .skip(skips)\
                .limit(page_size)
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while listing from the collection: {}: {}"
                                     .format(collection, str(err)))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def get_count(collection):
        current_app.logger.debug("Returns count of total collection: {}".format(collection))
        try:
            Database.client.server_info()
            return Database.DATABASE[collection].find().count()
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while counting the collection: {}: {}"
                                     .format(collection, str(err)))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def update(collection, filter_query, update_query):
        current_app.logger.debug("Updating to the collection: {}".format(collection))
        try:
            Database.client.server_info()
            Database.DATABASE[collection].update(filter_query, update_query)
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while updating to the collection: {}: {}"
                                     .format(collection, str(err)))
            current_app.logger.error("Exception: {}".format(err))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def delete(collection, filter_query):
        current_app.logger.debug("Deleting from the collection: {}".format(collection))
        try:
            Database.client.server_info()
            Database.DATABASE[collection].delete_one(filter_query)
            return True
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("Exception occurred while deleting from the collection: {}: {}"
                                     .format(collection, str(err)))
            current_app.logger.error("Exception: {}".format(err))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)

    @staticmethod
    def health():
        try:
            current_app.logger.debug("DB Server info: {}".format(str(Database.client.server_info())))
        except errors.ServerSelectionTimeoutError as err:
            current_app.logger.error("DB Connection Error: {}".format(str(err)))
            raise CustomErr(constants.DATABASE_NOT_AVAILABLE, 500)
