import requests
from .getVersion import get_version

def get_latest_champion_ddragon(champion_json, language="en_US"):
    if language in champion_json:
        return champion_json[language]

    response = None

    while response is None or response.status_code != 200:
        version = get_version()
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json")

    champion_json[language] = response.json()
    return champion_json[language]