from pymongo import MongoClient

def connect(db_name, mongo_uri):
    client=MongoClient(mongo_uri)
    return client[db_name]

def insert(connect_param, collection_data):
    database=connect(connect_param["db_name"], connect_param["mongo_uri"])
    
    for document in collection_data:
            database[document["dtype"]].insert_one(document)

def read(connect_param, collection_name, channel_id):
    database=connect(connect_param["db_name"], connect_param["mongo_uri"])

    return database[collection_name].find({"channel_id": channel_id})