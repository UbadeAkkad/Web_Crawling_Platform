from pymongo import MongoClient

def get_db_handle():

    client = MongoClient("mongodb://localhost:27017/")
    db = client.django

    return db