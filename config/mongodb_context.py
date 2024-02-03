from pymongo import MongoClient


def get_collection():
    """To return a collection (of contacts) from the local MongoDB database

    Returns:
        _type_: _description_
    """
    # TODO: store connection string as env variables!
    CONNECTION_STRING = ""
    client = MongoClient(CONNECTION_STRING)
    database = client['?']
    return database["?"]