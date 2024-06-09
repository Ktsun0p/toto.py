import requests
import os
import json
current_dir = os.path.dirname(os.path.abspath(__file__))
emblems_path = os.path.join(current_dir,"../data/emblems.json")

def get_rank_status(region, summoner_id, api_key):
    emblems = json.load(open(emblems_path))
    ranked_stats = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}').json()
    ranked_stats = [w for w in ranked_stats if w['queueType'] != "RANKED_TFT_PAIRS"]
    
    solo_q = [w for w in ranked_stats if w['queueType'] == "RANKED_SOLO_5x5"]
    flex_q = [w for w in ranked_stats if w['queueType'] == "RANKED_FLEX_SR"]
   
    ranked = []

    if solo_q:
        soloQ = {
            "queueType":"Solo/Duo",
            "tier": capitalizeFirstLetter(str(solo_q[0]['tier']).lower()),
            "rank":solo_q[0]['rank'],
            "emblem": emblems[str(solo_q[0]['tier']).lower()],
            "leaguePoints": solo_q[0]['leaguePoints'],
            "wins": solo_q[0]["wins"],
            "losses": solo_q[0]["losses"],
            "win_ratio": round((100*float(solo_q[0]["wins"])/(float(solo_q[0]["wins"])+float(solo_q[0]["losses"])))),
            "hotStreak":solo_q[0]['hotStreak']
        }
        ranked.append(soloQ)
    if flex_q:
        flexQ = {
            "queueType":"Flex",
            "tier": capitalizeFirstLetter(str(flex_q[0]['tier']).lower()),
            "rank":flex_q[0]['rank'],
            "emblem": emblems[str(flex_q[0]['tier']).lower()],
            "leaguePoints": flex_q[0]['leaguePoints'],
            "wins": flex_q[0]["wins"],
            "losses": flex_q[0]["losses"],
            "win_ratio": round((100*float(flex_q[0]["wins"]))/(float(flex_q[0]["wins"])+float(flex_q[0]["losses"]))),
            "hotStreak":flex_q[0]['hotStreak']
        }
        ranked.append(flexQ)
               
    return ranked

def capitalizeFirstLetter(text):
    return text[0].upper() + text[1:]
    