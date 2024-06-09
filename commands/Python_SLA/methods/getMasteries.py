import requests
from .getVersion import get_version
from .getChampByKey import get_champ_by_key

champion_by_id_cache = {}
champion_json = {}

masteries_emojis = [
    "<:m1:1244057161911373906>",
    "<:m2:1244057159659159583>",
    "<:m3:1244057156777410660>",
    "<:m4:1244057632885575770>",
    "<:m5:1244057634609565777>",
    "<:m6:1244057636220174366>",
    "<:m7:1244057637801169009>",
    "<:m8:1244057639462375536>",
    "<:m9:1244057642066772030>",
    "<:m10:1244057644638146632>"
    ]
def get_masteries(summoner_id, region, key, language="en_US"):
    last_ver = get_version()
    masteries = requests.get(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{summoner_id}?api_key={key}').json()
   
    champ_emojis = requests.get('https://ktsun0p.github.io/cakebot-simple-api/champs.json').json()
    top_masteries = []

    if masteries:
        counter = 0
        for mastery in masteries:
            if counter >= 10:
                break
            fm = get_champ_by_key(champion_by_id_cache, champion_json, mastery['championId'], language)
            fm1 = mastery['championLevel']
            pfm1 = mastery['championPoints']
            champ_emj = "<:Toto_Bug:1019280617105522729>" if str(mastery['championId']) not in champ_emojis else champ_emojis[str(mastery['championId'])]['icon']
            levelEmj = "<:m10:1244057644638146632>" if (fm1-1) >= 10 else masteries_emojis[fm1 - 1]
            top_masteries.append({
                'name': fm['name'],
                'id': fm['id'],
                'slogan': fm['title'],
                'level': fm1,
                'levelEmoji': levelEmj,
                'emoji': champ_emj,
                'points': pfm1,
                'full': f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{fm["id"]}_0.jpg',
                'square': f'http://ddragon.leagueoflegends.com/cdn/{last_ver}/img/champion/{fm["id"]}.png'
            })
            counter +=1
    return top_masteries