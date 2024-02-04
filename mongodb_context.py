from pymongo import MongoClient
import os

def get_collection():
    """To return a collection (of contacts) from the local MongoDB database

    Returns:
        pymongo.collection.Collection: the collection of a MongoDB database.
    """
    variable = "env var here"
    CONNECTION_STRING = os.getenv(variable)
    client = MongoClient(CONNECTION_STRING)
    database = client['database']
    return database["collection"]