from discord import InteractionType, app_commands
import discord
import discord.errors
import discord.http
from dotenv import load_dotenv
import os
from typing import Final
from commands.__init__ import setup_commands
from database import get_collection
from schems.server import Server
#from music import Music
from datetime import datetime
from emojis_cache import update_cache
load_dotenv()

TOKEN:Final[str] = os.getenv("DISCORD_TOKEN")
LOGIN_CHANNEL:Final[int] = os.getenv("LOGIN_CHANNEL")

ES_JOIN_CHANNEL:Final[int] = os.getenv("ES_JOIN_CHANNEL")
ES_COMMAND_CHANNEL:Final[int] = os.getenv("ES_COMMAND_CHANNEL")

EN_JOIN_CHANNEL:Final[int] = os.getenv("EN_JOIN_CHANNEL")
EN_COMMAND_CHANNEL:Final[int] = os.getenv("EN_COMMAND_CHANNEL")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)
#client.music = Music(client=client)
setup_commands(tree=tree)


@client.event
async def on_ready():
    custom = discord.CustomActivity("kats.uno/totobot")
    #print('Inicializando cliente de música...')
    #await client.music.initialize()
    #await handle_music_events(client=client)
    #print('Cliente de música inicializado.')
    print("Verificando el estado de la base de datos...")
    await check_servers_database()
    print("DB OKAY.")
    print('Cargando emojis...')
    await load_emojis()
    # print("Sincronizando command tree...")
    # await tree.sync()
    # print("Command Tree sincronizado.")
    await client.change_presence(status=discord.Status.dnd, activity=custom)
    print(f'{client.user} está listo.')
 
    channel = await client.fetch_channel(LOGIN_CHANNEL)
    now = datetime.now()
    date_string = now.strftime("`%d/%m/%Y` **%H:%M:%S**")
    ready_embed = discord.Embed(color=discord.Color.yellow())
    ready_embed.set_author(name=f"Successfully logged in as {client.user.display_name}",icon_url=client.user.display_avatar)
    ready_embed.description = f'In **{len(client.guilds)}** guilds.\n{date_string}'
    await channel.send(embed=ready_embed)  
    
@client.event
async def on_guild_join(guild:discord.Guild):
    
    collection =get_collection("servers")
    server_file = [s for s in collection.find({"server_id":guild.id})]    
    
    if server_file: return
    
    server = Server(server_id=guild.id)
    
    es_channel = await client.fetch_channel(ES_JOIN_CHANNEL)
    en_channel = await client.fetch_channel(EN_JOIN_CHANNEL)
    
    await server.to_database()
    
    server_embed = discord.Embed(color=discord.Color.yellow())
    server_embed.set_author(name="I successfully joined a new server!",icon_url=client.user.display_avatar)
    
    await en_channel.send(embed=server_embed)
    server_embed.set_author(name="¡Me uní a un nuevo servidor!",icon_url=client.user.display_avatar)
    await es_channel.send(embed=server_embed)
    pass   

@client.event
async def on_interaction(interaction:discord.Interaction):
    if interaction.type != InteractionType.application_command: return
    es_channel = await client.fetch_channel(ES_COMMAND_CHANNEL)
    en_channel = await client.fetch_channel(EN_COMMAND_CHANNEL)
    
    cmd_embed = discord.Embed(color=discord.Color.yellow())
    command = ''
    if(hasattr(interaction.command,'parent') and hasattr(interaction.command.parent,'name')):
        command = f'/{interaction.command.parent.name} {interaction.command.name}'
    elif(hasattr(interaction.command,'name')): command = f'/{interaction.command.name}'
    else: return
    en_text = f"Successfully executed command `{command}`."
    es_text = f"Comando `{command}` ejecutado correctamente."
    
    await en_channel.send(embed=cmd_embed.set_author(name=en_text,icon_url=client.user.display_avatar))
    await es_channel.send(embed=cmd_embed.set_author(name=es_text,icon_url=client.user.display_avatar))

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error,app_commands.CommandNotFound):
        return
    else:
        raise error

async def check_servers_database():
    collection = get_collection("servers")
    guilds = client.guilds
    for guild in guilds:
        guild_archive = [s for s in collection.find({"server_id":f'{guild.id}'})]
        if not guild_archive:
            server = Server(server_id=guild.id)
            await server.to_database()
            print(f"Added guild: {guild.id} to the DB.")

async def load_emojis():
    emojis = await client.http.request(discord.http.Route('GET', '/applications/{application_id}/emojis', application_id=client.application_id))
    update_cache(emojis=emojis)
    print('Emojis cargados.')
client.run(token=TOKEN)