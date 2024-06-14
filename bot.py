from discord import app_commands
import discord
import discord.errors
from dotenv import load_dotenv
import os
from typing import Final
from commands.__init__ import setup_commands
from database import get_collection
from schems.server import Server
from datetime import datetime
from music import Music
load_dotenv()

TOKEN:Final[str] = os.getenv("DISCORD_TOKEN")
JOIN_CHANNEL:Final[int] = os.getenv("JOIN_CHANNEL")
LOGIN_CHANNEL:Final[int] = os.getenv("LOGIN_CHANNEL")
COMMAND_CHANNEL:Final[int] = os.getenv("COMMAND_CHANNEL")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client=client)
client.music = Music(client=client)
setup_commands(tree=tree)

@client.event
async def on_ready():
    custom = discord.CustomActivity("TotoBot")
    print('Inicializando cliente de música...')
    await client.music.initialize()
    print('Cliente de música inicializado.')
    print("Verificando el estado de la base de datos")
    await check_servers_database()
    print("DB OKAY.")
    print("Sincronizando command tree...")
    await tree.sync()
    print("Command Tree sincronizado.")
    await client.change_presence(status=discord.Status.dnd, activity=custom)
    print(f'{client.user} está listo.')

    # channel = await client.fetch_channel(LOGIN_CHANNEL)
    # now = datetime.now()
    # date_string = now.strftime("`%d/%m/%Y` **%H:%M:%S**")
    # ready_embed = discord.Embed(color=discord.Color.yellow())
    # ready_embed.set_author(name=f"Successfully logged in as {client.user.display_name}",icon_url=client.user.display_avatar)
    # ready_embed.description = f'In **{len(client.guilds)}** guilds.\n **{len(client.users)}** users.\n{date_string}'
    # await channel.send(embed=ready_embed)  
    
@client.music.event
async def add_song(interaction:discord.Interaction,channel,song_info):
    autoplay = client.music.autoplay[interaction.guild_id]
    loop = client.music.loop[interaction.guild_id]
    a_status = 'enabled' if autoplay else 'disabled'
    l_status = 'enabled' if loop else 'disabled'
    added_embed = discord.Embed(color=discord.Color.yellow(),url=song_info['link'])
    added_embed.set_author(name='🎧 Added song...',icon_url=client.user.display_avatar)
    added_embed.title = f'**{song_info['title']}**'
    added_embed.description = f'Duration: **{song_info['duration']}**\nAutoplay: **{a_status}**. Loop: **{l_status}**.'
    added_embed.set_thumbnail(url=song_info['thumbnail'])
    added_embed.set_footer(text=interaction.user.display_name,icon_url=interaction.user.display_avatar)
    msg = await interaction.original_response()
    await msg.edit(content='',embed=added_embed)   
     
@client.music.event
async def play_song(interaction:discord.Interaction,channel,song_info, is_next_in_playlist:bool):
    autoplay = client.music.autoplay[interaction.guild_id]
    loop = client.music.loop[interaction.guild_id]
    a_status = 'enabled' if autoplay else 'disabled'
    l_status = 'enabled' if loop else 'disabled'
    now_playing_embed = discord.Embed(color=discord.Color.yellow(),url=song_info['link'])
    now_playing_embed.set_author(name='🎧 Now playing...',icon_url=client.user.display_avatar)
    now_playing_embed.title = f'**{song_info['title']}**'
    now_playing_embed.description =  f'Duration: **{song_info['duration']}**\nAutoplay: **{a_status}**. Loop: **{l_status}**.'
    now_playing_embed.set_thumbnail(url=song_info['thumbnail'])
    now_playing_embed.set_footer(text=interaction.user.display_name,icon_url=interaction.user.display_avatar)
    if is_next_in_playlist:
        channel = interaction.channel
        await channel.send(embed=now_playing_embed,content='') 
    elif is_next_in_playlist == False:
        msg = await interaction.original_response()
        await msg.edit(embed=now_playing_embed, content='') 
            
@client.music.event
async def song_skipped(interaction:discord.Interaction, is_next_song:bool):
    msg = await interaction.original_response()
    skip_embed = discord.Embed(color=discord.Color.yellow())
    if is_next_song:
        skip_embed.set_author(name='Song skipped, playing next song.', icon_url=client.user.display_avatar)
        await msg.edit(embed=skip_embed)
    else:
        skip_embed.set_author(name="Song skipped, there are not more songs in the queue.", icon_url=client.user.display_avatar)
        await msg.edit(embed=skip_embed) 
        
@client.music.event
async def music_error(interaction:discord.Interaction, error:str):
    msg = await interaction.original_response()
    error_embed = discord.Embed(color=discord.Color.red())
    if error == 'connection':
        error_embed.set_author(name='Connection error: couldn\'t connect to your voice channel.', icon_url=interaction.user.display_avatar)
    if error == 'download':
        error_embed.set_author(name='Download error: try again or provide a valid URL.', icon_url=interaction.user.display_avatar)    
    await msg.edit(embed=error_embed)    
    if error == 'playback':
        error_embed.set_author(name='Playback error: try again or provide a valid URL.', icon_url=interaction.user.display_avatar)    
    if error == 'playlist':
        error_embed.set_author(name='Playlist error: try again or provide a valid URL.', icon_url=interaction.user.display_avatar)          
    await msg.edit(embed=error_embed)
    
@client.event
async def on_guild_join(guild:discord.Guild):
    
    collection =get_collection("servers")
    server_file = [s for s in collection.find({"server_id":guild.id})]    
    
    if server_file: return
    
    server = Server(server_id=guild.id)
    channel = await client.fetch_channel(JOIN_CHANNEL)
    
    await server.to_database()
    
    server_embed = discord.Embed(color=discord.Color.yellow())
    server_embed.set_author(name="I successfully joined a new server!",icon_url=client.user.display_avatar)
    
    await channel.send(embed=server_embed)
    pass   
    
# @tree.error
# async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
#     if isinstance(error,app_commands.CommandInvokeError):
#         print(error)
#         pass
#     else:
#         raise error

async def check_servers_database():
    collection = get_collection("servers")
    guilds = client.guilds
    for guild in guilds:
        guild_archive = [s for s in collection.find({"server_id":guild.id})]
        if not guild_archive:
            server = Server(server_id=guild.id)
            await server.to_database()
            print(f"Added guild: {guild.id} to the DB.")
            
        
    

client.run(token=TOKEN)