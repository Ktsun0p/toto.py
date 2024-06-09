import requests
import re
from .getChampByKey import get_champ_by_key

def get_live_game(champion_by_id_cache, champion_json, region, puuid, api_key):
    live_game = requests.get(f'https://{region}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={api_key}').json()
    game = False
    if 'gameId' not in live_game:
        return game
    
    queues_id = requests.get('https://static.developer.riotgames.com/docs/lol/queues.json').json()
    champ_emojis = requests.get('https://ktsun0p.github.io/cakebot-simple-api/champs.json').json()
   
    summoner = [p for p in live_game['participants'] if p['puuid'] == puuid]
    gamemode = [w for w in queues_id if w['queueId'] == live_game['gameQueueConfigId']]

    live_game_champ = get_champ_by_key(champion_by_id_cache=champion_by_id_cache,champion_json=champion_json,key=summoner[0]['championId'])

    gamemode_description = str(gamemode[0]['description']).replace(" games","")
    game = {
        'mode': gamemode_description,
        'champion':{
            'name':live_game_champ['name'],
            'id': summoner[0]['championId'],
            'emoji': champ_emojis[str(summoner[0]['championId'])]["icon"]
        }
    } 
    return game

