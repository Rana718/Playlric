from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

Mongo_url = os.getenv('MONGO_URL')
db_name = os.getenv('MONGO_NAME')

def get_mongo_clinet():
    clinet = MongoClient(Mongo_url)
    mongo_db_name = db_name
    db = clinet[mongo_db_name]

    return db

