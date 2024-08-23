from .methods.getSummonerByName import get_summoner_by_name
from .methods.getSummonerByPUUID import get_summoner_by_puuid
import json
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
regions_path = os.path.join(current_dir,"./data/regions.json")
regions = json.load(open(regions_path))
class riot_api:
    def __init__(self, api_key):
        self.key = api_key

    class Summoner:
        def __init__(self, api_instance, name:str, tag:str, region:str, puuid:str):
            self.api_instance = api_instance
            self.name = name
            self.tag = tag
            self.region = region
            self.puuid = puuid

        class LolProfile:
            def __init__(self, summoner):
                self.summoner = summoner

            def by_name(self):
                return get_summoner_by_name(name=self.summoner.name, tag=self.summoner.tag, region=self.summoner.region, apiInstance=self.summoner.api_instance)

            def by_puuid(self):
                return get_summoner_by_puuid(puuid=self.summoner.puuid, region=self.summoner.region, apiInstance=self.summoner.api_instance)

        def get_lol_profile(self):
            return self.LolProfile(self)
    def get_regions(self):
        return regions
    
    def create_summoner(self, name, tag, region,puuid):
        return self.Summoner(self, name, tag, region,puuid)