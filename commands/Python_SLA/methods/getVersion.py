import requests

def get_version():
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    last_ver = response.json()[0]
    return last_ver