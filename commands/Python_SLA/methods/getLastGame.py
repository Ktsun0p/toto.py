import requests
import json
from .handleAPIError import handle_api_error
from .getChampByKey import get_champ_by_key

champion_by_id_cache = {}
champion_json = {}

def get_last_game(region_routing_value, puuid, api_key, lang = "en_US"):
    last_game_id = requests.get(f'https://{region_routing_value}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=1&api_key={api_key}').json()
   
    if 'status' in last_game_id:
        return handle_api_error(last_game_id['status']['status_code'])
    last_game_id = last_game_id[0]

    last_game = requests.get(f'https://{region_routing_value}.api.riotgames.com/lol/match/v5/matches/{last_game_id}?api_key={api_key}').json()
    if 'status' in last_game:
        return handle_api_error(last_game['status']['status_code'])
    
    last_game_info = [p for p in last_game['info']['participants'] if p['puuid'] == puuid]
    
    queues_id = requests.get('https://static.developer.riotgames.com/docs/lol/queues.json').json()
    champ_emojis = requests.get('https://ktsun0p.github.io/cakebot-simple-api/champs.json').json()
    gamemode = [w for w in queues_id if w['queueId'] == last_game['info']['queueId']]

    gamemode_description = str(gamemode[0]['description']).replace(" games","")

    kd = (last_game_info[0]['kills'] + last_game_info[0]['assists']) / (1 if last_game_info[0]['deaths'] == 0 else last_game_info[0]['deaths'])

    kda = round((kd + 1e-15) * 100) / 100
    last_game_champ = get_champ_by_key(champion_by_id_cache, champion_json, last_game_info[0]['championId'], lang)
    last_game_champ_emoji = champ_emojis[str(last_game_info[0]['championId'])]['icon']
    
    LANE_EMJ = {
        'TOP': "<:TOP:977294915841187922>",
        "JUNGLE":"<:JUNGLE:977294894169210891>",
        "MIDDLE":"<:MID:977294933453049956>",
        "BOTTOM":"<:ADC:977294965870829658><:SUPPORT:977294998217318471>"
    }
    lane_emoji = "<:Toto_Bug:1019280617105522729>" if str(last_game_info[0]['lane']) not in LANE_EMJ else LANE_EMJ[last_game_info[0]['lane']]
    last_game_resumed = {
    'mode': gamemode_description,
    'win': last_game_info[0]['win'],
    'champion': last_game_champ['name'],
    'emoji': last_game_champ_emoji,
    'kills': last_game_info[0]['kills'],
    'deaths': last_game_info[0]['deaths'],
    'assists': last_game_info[0]['assists'],
    'lane': last_game_info[0]['lane'],
    'id': last_game['info']['gameId'],
    'laneEmoji': lane_emoji,
    'visionscore': last_game_info[0]['visionScore'],
    'kda': kda
    }
    return last_game_resumed