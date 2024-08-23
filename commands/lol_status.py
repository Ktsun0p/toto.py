from discord import app_commands, Interaction
import discord
from dotenv import load_dotenv
import os
from typing import Final
from .Python_SLA.main import riot_api
load_dotenv()
from urllib import request, error
from cooldown_manager import CooldownManager
import requests
cooldown_manager = CooldownManager()

TOKEN:Final[str] = os.getenv("RIOT_TOKEN")
api = riot_api(api_key=TOKEN)
regions_json = api.get_regions()

lol_regions = [
    app_commands.Choice(name="Brazil (BR)", value="BR1"),
    app_commands.Choice(name="Europe Nordic & East (EUNE)", value="EUN1"),
    app_commands.Choice(name="Europe West (EUW)", value="EUW1"),
    app_commands.Choice(name="Japan (JP)", value="JP1"),
    app_commands.Choice(name="Republic of Korea (KR)", value="KR"),
    app_commands.Choice(name="Latin America North (LAN)", value="LA1"),
    app_commands.Choice(name="Latin America South (LAS)", value="LA2"),
    app_commands.Choice(name="North America (NA)", value="NA1"),
    app_commands.Choice(name="Oceania (OCE)", value="OC1"),
    app_commands.Choice(name="Turkey (TR)", value="TR1"),
    app_commands.Choice(name="Russia (RU)", value="RU"),
    app_commands.Choice(name="Philippines (PH)", value="PH2"),
    app_commands.Choice(name="Singapore, Malaysia and Indonesia (SG)", value="SG2"),
    app_commands.Choice(name="Thailand (TH)", value="TH2"),
    app_commands.Choice(name="Taiwan, Hong Kong and Macau (TW)", value="TW2"),
    app_commands.Choice(name="Vietnam (VN)", value="VN2")
    ]

servers = {
    "BR1": f'https://br1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "EUN1": f'https://eun1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "EUW1": f'https://euw1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "JP1": f'https://jp1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "KR": f'https://kr.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "LA1": f'https://la1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "LA2": f'https://la2.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "ME1": f'https://me1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "NA1": f'https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "OC1": f'https://oc1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "PH2": f'https://ph2.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "RU": f'https://ru.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "SG2": f'https://sg2.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "TH2": f'https://th2.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "TR1": f'https://tr1.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}',
    "VN2": f'https://vn2.api.riotgames.com/lol/status/v4/platform-data?api_key={TOKEN}'
}

@app_commands.choices(region=lol_regions)
async def status_command(interaction: Interaction,region:str):
    await interaction.response.defer()
    msg = await interaction.original_response()
    servers_status = await get_lol_status(region=region)
    embed = discord.Embed()
    embed.set_author(name=interaction.client.user.display_name,icon_url=interaction.client.user.display_avatar)
    embed.description = servers_status
    embed.color = discord.Color.gold()
    return await msg.edit(embed=embed)

async def get_lol_status(region:str):
    chosen_server = servers[region]
    response = requests.get(chosen_server).json()
    try:
        response_status = request.urlopen(chosen_server)     
    except error.HTTPError as e:
        text = f'{regions_json[region][0]}: 🔴 Offline'
    else: text = f'{response['name']}: 🟢 Online'
    return text