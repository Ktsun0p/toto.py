from .getLatestChampionDDragon import get_latest_champion_ddragon

def get_champ_by_key(champion_by_id_cache, champion_json, key, language="en_US"):
    if language not in champion_by_id_cache:
        json = get_latest_champion_ddragon(champion_json, language)

        champion_by_id_cache[language] = {}
        for champion_name in json['data']:
            champ_info = json['data'][champion_name]
            champion_by_id_cache[language][champ_info['key']] = champ_info
    return champion_by_id_cache[language][str(key)]