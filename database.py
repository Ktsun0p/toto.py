import pymongo
from dotenv import load_dotenv
import os
from typing import Final
load_dotenv()

MONGO_URI:Final[str] = os.getenv("MONGO_URI")
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client.TotoBot

def get_collection(name:str):
    return db[name]
