import pymongo.collection
from database import get_collection
import pymongo
class Summoner():
    def __init__(self,user_id:int, puuid:str, region:str) -> None:
        self.user_id = user_id
        self.puuid = puuid
        self.region = region

    def to_dict(self):
           return {
            "user_id": self.user_id,
            "puuid": self.puuid,
            "region": self.region
        }
    async def to_database(self):
        collection:pymongo.collection.Collection = get_collection("summoners")
        return collection.insert_one(self.to_dict())

