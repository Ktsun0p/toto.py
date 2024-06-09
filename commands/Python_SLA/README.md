# Simplified Riot API

A simplified version of the LoL api, so you don't have to read all the documentation and just simply get all the info from the summoner's name, tag and region.
I made this for my Discord bot TotoBot, whose main feature is the interaction with the league of legend api.
You're free to download this and put it into your project. It requires a token from the riot developer portal in order to work.
If you want to give some support you can invite TotoBot to your server and i'll be extremely happy. https://kats.uno/totobot

## Usage

#### Initialize api

```python
from sra.main import riot_api
api = riot_api(api_key="YOUR_API_KEY")
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get summoner with name and region

```python
  sumoner = api.create_summoner(name="Ktsun0p",tag="Kts0p",region="LA2")

```

| Parameter | Type     | Description                   |
| :-------- | :------- | :---------------------------- |
| `name`    | `string` | **Required**. Summoner name   |
| `tag`     | `string` | **Required**. Summoner tag    |
| `region`  | `string` | **Required**. Summoner region |

## Dependencies

**Requires `requests` to work properly**

## Example

```python
api = riot_api(api_key="API_KEY")
sumoner1 = api.create_summoner(name="Ktsun0p",tag="Kts0p",region="LA2").get_lol_profile.by_name()
summoner2 = api.create_summoner(puuid="PUUID", region="LA2").get_lol_profile.by_puuid()
print(json.dumps(summoner1,indent=4))
print(json.dumps(summoner2,indent=4))
```
