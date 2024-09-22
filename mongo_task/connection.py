from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_connection():
    return MongoClient(
        "mongodb://root:password@mongo/?retryWrites=true&w=majority",
        server_api=ServerApi("1"),
    )