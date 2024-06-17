import pymongo.collection
from database import get_collection
import pymongo
class Server():
    def __init__(self, server_id:int, music_channel:int = None, music_role:int = None) -> None:
        self.server_id = server_id
        self.music_channel = music_channel
        self.music_role = music_role

    def to_dict(self):
           return {
            "server_id": f'{self.server_id}',
            "music_settings": {
                 "channel": f'{self.music_channel}',
                 "role": f'{self.music_role}'
            }
        }
    async def to_database(self):
        collection:pymongo.collection.Collection = get_collection("servers")
        return collection.insert_one(self.to_dict())

