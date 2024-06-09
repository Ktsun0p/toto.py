import requests
import json
import os
from .getVersion import get_version
from .getMasteries import get_masteries
from .handleAPIError import handle_api_error
from .getLiveGame import get_live_game
from .getLastGame import get_last_game
from .getRankStatus import get_rank_status
champion_by_id_cache = {}
champion_json = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
regions_path = os.path.join(current_dir,"../data/regions.json")

def get_summoner_by_name(name, tag,region, apiInstance, lang = "en_US"):
    region = region.upper()
    api_key = apiInstance.key
    regions = json.load(open(regions_path))
    
    if region not in regions:
        raise Exception(f'Region "{region}" does not exist.')
    last_ver = get_version()

    region_routing_value = regions[region][1]
    region_name = regions[region][0]

    try:
       riot_url = requests.get(f'https://{region_routing_value}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}').json()

       if 'status' in riot_url:
           handle_api_error(riot_url['status']['status_code'])

       summoner_url = requests.get(f'https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{riot_url['puuid']}?api_key={api_key}') .json()
       if 'status' in summoner_url:
           handle_api_error(summoner_url['status']['status_code'])

       top_masteries = get_masteries(summoner_id=summoner_url["puuid"],region=region,key=api_key) 
       live_game = get_live_game(champion_by_id_cache=champion_by_id_cache,champion_json=champion_json,region=region,puuid=summoner_url['puuid'],api_key=api_key)
       last_game = get_last_game(region_routing_value=region_routing_value,puuid=summoner_url['puuid'],api_key=api_key)
       rank_status = get_rank_status(region=region,summoner_id=summoner_url['id'],api_key=api_key)
       summoner = {
       "name":riot_url["gameName"],
       "tag":riot_url["tagLine"],
       "region":region_name,
       "id":summoner_url["id"],
       "accountId":summoner_url["accountId"],
       "puuid":summoner_url["puuid"],
       "level":summoner_url['summonerLevel'],
       "profileIcon":f'https://ddragon.leagueoflegends.com/cdn/{last_ver}/img/profileicon/{summoner_url["profileIconId"]}.png?width=256&height=256',
       "liveGame":live_game,
       "lastGame": last_game,
       "ranked":rank_status,
       "top_masteries":top_masteries
       }

       return json.dumps(summoner)
    except Exception as e:
        raise Exception(str(e))