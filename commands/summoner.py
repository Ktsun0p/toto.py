from discord import app_commands, Interaction, ui
import discord
from dotenv import load_dotenv
import os
import json
from typing import Final
from .Python_SLA.main import riot_api
from schems.summoner import Summoner
from database import get_collection
load_dotenv()
TOKEN:Final[str] = os.getenv("RIOT_TOKEN")
api = riot_api(api_key=TOKEN)

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

async def format_summoner_data(interaction: Interaction, name:str, tag:str, region:str, puuid:str):
    if not interaction.response.is_done():
        await interaction.response.defer()
    msg = await interaction.original_response()
    try:
        summoner = json.loads(api.create_summoner(name=name,tag=tag,region=region,puuid=None).get_lol_profile().by_name()) if puuid is None else json.loads(api.create_summoner(name=None,tag=None,region=region,puuid=puuid).get_lol_profile().by_puuid())
        #Separate the information in various groups for later use.
        top_ten_masteries = summoner["top_masteries"][:10] #Top 10 masteries
        summoner_name = summoner["name"]
        summoner_icon_url = summoner["profileIcon"]
        ranked_info = summoner["ranked"] #Ranked Info
        last_game = summoner["lastGame"] #Last Game info
        live_game = summoner["liveGame"] #Is playing? Current game info
        #Create the Embeds
        summoner_embed = discord.Embed(color=discord.Color.yellow())
        top_masteries_embed = discord.Embed(color=discord.Color.yellow())
        #Create the buttons
        buttons = create_button(embed=top_masteries_embed,message=msg)

        
        #Format top 10 masteries
        formatted_top_masteries = []
        for i, item in enumerate(top_ten_masteries):
            formatted_champion = f'{item["emoji"]} {i+1}. {item["name"]} ({item["level"]}) {item["levelEmoji"]} ({item["points"]:,})'
            formatted_top_masteries.append(formatted_champion)
        #Format ranked stats
        formatted_ranks =[]
        for i, item in enumerate(ranked_info):
            formatted_rank = f'**{item["queueType"]}**:\n ** {item["emblem"]} {item["tier"]} {item["rank"]}: {item["leaguePoints"]} LP. {item["wins"]}W {item["losses"]}L. {item["win_ratio"]}% WR.**'
            formatted_ranks.append(formatted_rank)

        author = f"[{summoner["level"]}] {summoner_name} [{summoner["region"]}]"
        top_masteries_msg = "\n".join(formatted_top_masteries[:3]) if formatted_top_masteries != [] else "None."
        top_mastery_img = top_ten_masteries[0]["full"] if formatted_top_masteries[0] != [] else "https://cdn.discordapp.com/banners/953418385440509974/11b72fe14026e3ec0106baab9ed13fcd.png?size=2048"
        ranked_info_msg = "\n".join(formatted_ranks) if formatted_ranks != [] else "Unranked."
        top_ten_masteries_msg = "\n".join(formatted_top_masteries)

        #Build embeds
        top_masteries_embed.set_author(name=f"{summoner_name}: Best champions", icon_url=summoner_icon_url, url=summoner_icon_url)
        top_masteries_embed.description = top_ten_masteries_msg
        buttons.embed = top_masteries_embed
        summoner_embed.set_author(icon_url=summoner_icon_url,name=author,url=summoner_icon_url)
        summoner_embed.add_field(name='<:m10:1244057644638146632> Top Masteries:', value=top_masteries_msg, inline=True)
        summoner_embed.add_field(name='<:challenger_emblem:1024786065866891404> Ranked Info:', value=ranked_info_msg,inline=True)
        summoner_embed.set_image(url=top_mastery_img)
        #If there's a last game, add it to the embed.
        if last_game != []:
            result = "🟢 Victory" if last_game["win"] == True else "🔴 Defeat"
            last_game_msg = f"{result} **{last_game["mode"]}** as **{last_game["emoji"]} {last_game["champion"]} {last_game["laneEmoji"]}, {last_game["kills"]}/{last_game["deaths"]}/{last_game["assists"]} ({last_game["kda"]}), {last_game["visionscore"]} <:vision_score:980429093143207946>**"
            summoner_embed.add_field(name="<:toto:976688374901526589> Last Game:", value=last_game_msg, inline=False)
            buttons.add_item(ui.Button(label='Last Game', style=discord.ButtonStyle.url, url=f"https://www.leagueofgraphs.com/en/match/{summoner["region"].lower()}/{last_game["id"]}", emoji="<:porofessor:1020879341158137977>"))
        #If is in game, add it to the embed.
        if live_game != False:
            live_game_champion = live_game["champion"]
            live_game_msg = f"Playing **{live_game["mode"]}** as **{live_game_champion["emoji"]} {live_game_champion["name"]}**"
            summoner_embed.add_field(name="🌿 Live Game:", value=live_game_msg, inline=False)
            buttons.add_item(ui.Button(label='Live Game', style=discord.ButtonStyle.url, url=f"https://porofessor.gg/en/live/{summoner["region"].lower()}/{summoner_name}-{tag}", emoji="<:porofessor:1020879341158137977>"))
        #Finally returns formatted the collected data.
        return await msg.edit(embed=summoner_embed,view=buttons)
    except Exception as e:
     print(e)
     error_str:str = e.args[0].replace("'", '"')
     try:
        error_dict = json.loads(error_str)
        if 'code' in error_dict:
            err_msg = "Unknown error."
            if(error_dict['code'] == 404): err_msg = f"Specified summoner don't exists, not in {region}."
            else: err_msg = f"**League of Legends API error, please try again later.**"
            err_embed = discord.Embed(color=discord.Color.red())
            err_embed.set_author(name=err_msg,icon_url=interaction.client.user.display_avatar.url)     
            return await msg.edit(embed=err_embed)
        else:
            err_embed = discord.Embed(description="**Unknown error, please report this at the [support server](https://kats.uno/totobot/support)**",color=discord.Color.red())
            err_embed.set_author(name="TotoBot",icon_url=interaction.client.user.display_avatar.url)     
            return await msg.edit(embed=err_embed)
     except Exception as e:
        print(e)
        err_embed = discord.Embed(description="**Unknown error, please report this at the [support server](https://kats.uno/totobot/support)**",color=discord.Color.red())
        err_embed.set_author(name="TotoBot",icon_url=interaction.client.user.display_avatar.url)     
        return await msg.edit(embed=err_embed)

@app_commands.describe(name="Summoner's name.")
@app_commands.describe(tag="Summoner's tag.")
@app_commands.describe(region="Summoner's region.")
@app_commands.choices(region=lol_regions)
async def summoner_get_command(interaction: Interaction, name:str, tag:str, region:str):
    return await format_summoner_data(interaction=interaction,name=name,tag=tag,region=region,puuid=None)
    

async def summoner_me_command(interaction:Interaction):
    await interaction.response.defer()
    msg = await interaction.original_response()
    USER_ID = interaction.user.id
    user_embed = discord.Embed(color=discord.Color.yellow()) 
    try:
        collection = get_collection("summoners")
        summoner_file = [s for s in collection.find({"user_id":USER_ID})]

        if not summoner_file: 
            user_embed.set_author(name='You don\'t have a LoL account linked.',icon_url=interaction.client.user.display_avatar)
            user_embed.description = 'Use `/summoner link` to link one.'
            return await msg.edit(embed=user_embed)
        summoner_file = summoner_file[0]
        puuid = summoner_file['puuid']
        region = summoner_file['region']
        return await format_summoner_data(interaction=interaction, name=None,tag=None,region=region,puuid=puuid)
    
    except Exception as e:
        user_embed.set_author(name='An unexpected error ocurred.',icon_url=interaction.client.user.display_avatar)
        user_embed.description = 'Please report it to our **[support server](https://kats.uno/totobot/support)**.'
        return await msg.edit(embed=user_embed)
        

    

@app_commands.describe(user="Select the user.")
async def summoner_user_command(interaction: Interaction, user:discord.User):
    await interaction.response.defer()
    msg = await interaction.original_response()
    USER_ID = user.id
    user_embed = discord.Embed(color=discord.Color.yellow())
    try:
        collection = get_collection("summoners")
        summoner_file = [s for s in collection.find({"user_id":USER_ID})]

        if not summoner_file: 
            user_embed.set_author(name=f'{user.display_name} does not have their LoL account connected to Discord.',icon_url=interaction.client.user.display_avatar)
            user_embed.description = 'Tell them to use `/summoner link`'
            return await msg.edit(embed=user_embed)
        summoner_file = summoner_file[0]
        puuid = summoner_file['puuid']
        region = summoner_file['region']
        return await format_summoner_data(interaction=interaction, name=None,tag=None,region=region,puuid=puuid)
    
    except Exception as e:
        user_embed.set_author(name='An unexpected error ocurred.',icon_url=interaction.client.user.display_avatar)
        user_embed.description = 'Please report it to our **[support server](https://kats.uno/totobot/support)**.'
        return await msg.edit(embed=user_embed)
     

async def summoner_unlink_command(interaction:Interaction):
    await interaction.response.defer()
    msg = await interaction.original_response()
    USER_ID = interaction.user.id
    user_embed = discord.Embed(color=discord.Color.yellow())
    try:
        collection = get_collection("summoners")
        summoner_file =  [s for s in collection.find({"user_id":USER_ID})]
        if not summoner_file: 
            user_embed.set_author(name='You don\'t have a LoL account linked.',icon_url=interaction.client.user.display_avatar)
            user_embed.description = 'Use `/summoner link` to link one.'
            return await msg.edit(embed=user_embed)
      
        collection.delete_one({"user_id":USER_ID})

        user_embed.set_author(name='LoL account successfully unlinked',icon_url=interaction.client.user.display_avatar)
        user_embed.description = 'Link again using `/summoner link`'
        return await msg.edit(embed=user_embed)

    except Exception as e:
        print(e)

@app_commands.describe(name="Summoner's name.")
@app_commands.describe(tag="Summoner's tag.")
@app_commands.describe(region="Summoner's region.")
@app_commands.choices(region=lol_regions)
async def summoner_link_command(interaction: Interaction, name:str, tag:str, region:str):
        await interaction.response.defer()
        msg = await interaction.original_response()
        USER_ID = interaction.user.id
        summoner_embed = discord.Embed(color=discord.Color.yellow())
        try:
            collection = get_collection("summoners")
            already_linked = [s for s in collection.find({"user_id":USER_ID})]

            if(already_linked): 
                summoner_embed.set_author(name=f'You already have a summoner linked to your account.',icon_url=interaction.client.user.display_avatar)
                summoner_embed.description = "Use `/summoner unlink` first."
                return await msg.edit(embed=summoner_embed)
            
            summoner = json.loads(api.create_summoner(name=name,tag=tag,region=region,puuid=None).get_lol_profile().by_name())
            summoner_name = summoner['name']
            summoner_tag = summoner['tag']
            summoner_icon_url = summoner['profileIcon']
            summoner_region = summoner['region']
            PUUID = summoner["puuid"]
            REGION = region
            
            await Summoner(user_id=USER_ID,puuid=PUUID,region=REGION).to_database()
            
            summoner_embed.set_author(name=f'I have successfully linked {summoner_name}#{summoner_tag} from {summoner_region} to your Discord account.',icon_url=summoner_icon_url)
            summoner_embed.description = f'Now you can use `/summoner me`'
            return await msg.edit(embed=summoner_embed)
        except Exception as e:
            error_str = e.args[0].replace("'", '"')
            err_embed = discord.Embed(description="**Unknown error, please report this at the [support server](https://kats.uno/totobot/support)**",color=discord.Color.red())
            err_embed.set_author(name="TotoBot",icon_url=interaction.client.user.display_avatar.url)               
            try:
                error_dict = json.loads(error_str)
                if 'code' in error_dict:
                    err_msg = "Unknown error."
                    if(error_dict['code'] == 404): err_msg = f"Specified summoner don't exists, not in {region}."
                    else: err_msg = f"**League of Legends API error, please try again later.**"
                    error_embed = discord.Embed(color=discord.Color.red())
                    error_embed.set_author(name=err_msg,icon_url=interaction.client.user.display_avatar.url)     
                    return await msg.edit(embed=error_embed)
                else:
                    return await msg.edit(embed=err_embed)
            except Exception as e:    
                return await msg.edit(embed=err_embed)
          
                
  

        
       
class create_button(ui.View):
    def __init__(self,*,timeout = 60, embed: discord.Embed, message: discord.InteractionMessage):
        super().__init__(timeout=timeout)
        self.embed = embed
        self.message = message
        
    async def on_timeout(self) -> None:
        self.red_button.disabled = True
        await self.message.edit(view=self)
        return await super().on_timeout()
    
    @discord.ui.button(label="Masteries",style=discord.ButtonStyle.blurple,emoji="<:m10:1244057644638146632>") 
    async def red_button(self,interaction:Interaction,button:ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=self.embed)
       
       
