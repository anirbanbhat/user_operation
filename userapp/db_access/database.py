from pymongo import MongoClient
from flask import current_app


class Database(object):
    DATABASE = None

    @staticmethod
    def initialize(host, port, db):
        client = MongoClient(host=host, port=int(port))
        Database.DATABASE = client[db]

    @staticmethod
    def insert(collection, data):
        current_app.logger.debug("Inserting to the collection: {}".format(collection))
        try:
            Database.DATABASE[collection].insert(data)
            return True
        except Exception as e:
            current_app.logger.error("Exception occurred while inserting to the collection: {}".format(collection))
            current_app.logger.error("Exception: {}".format(e))
            return False

    @staticmethod
    def get(collection, query):
        current_app.logger.debug("Retrieving from the collection: {}".format(collection))
        try:
            return Database.DATABASE[collection].find(query)
        except Exception as e:
            current_app.logger.error("Exception occurred while retrieving from the collection: {}".format(collection))
            current_app.logger.error("Exception: {}".format(e))
            raise e

    @staticmethod
    def get_all(collection, filter_query, projection_query):
        current_app.logger.debug("Listing all and projecting from the collection: {}".format(collection))
        try:
            return Database.DATABASE[collection].find(filter_query, projection_query)
        except Exception as e:
            current_app.logger.error("Exception occurred while listing from the collection: {}".format(collection))
            current_app.logger.error("Exception: {}".format(e))
            raise e

    @staticmethod
    def update(collection, filter_query, update_query):
        current_app.logger.debug("Updating to the collection: {}".format(collection))
        try:
            Database.DATABASE[collection].update(filter_query, update_query)
            return True
        except Exception as e:
            current_app.logger.error("Exception occurred while updating to the collection: {}".format(collection))
            current_app.logger.error("Exception: {}".format(e))
            return False

    @staticmethod
    def delete(collection, filter_query):
        current_app.logger.debug("Deleting from the collection: {}".format(collection))
        try:
            Database.DATABASE[collection].delete(filter_query)
            return True
        except Exception as e:
            current_app.logger.error("Exception occurred while deleting from the collection: {}".format(collection))
            current_app.logger.error("Exception: {}".format(e))
            return False
