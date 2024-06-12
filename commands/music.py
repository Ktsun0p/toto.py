from discord import app_commands, Interaction
import discord
from music import Music

@app_commands.describe(song='The song title.')
async def play_command(interaction: Interaction, song:str):
    client = interaction.client
    music:Music = client.music
    id = interaction.guild_id
    await interaction.response.defer()
    msg = await interaction.original_response()
    try:
       voice_channel = interaction.user.voice.channel
    except:
        return await msg.edit(content="You're not in a voice channel.")

    if(music.is_connected(interaction=interaction) and music.voice_channel[id].channel.id != voice_channel.id):
        return await msg.edit(content="I'm already connected in another channel.") 
    await music.play_music(interaction=interaction,song=song,voice_channel=voice_channel)
 
async def skip_command(interaction: Interaction):
    client = interaction.client
    music:Music = client.music
    id = interaction.guild_id
    await interaction.response.defer()
    msg = await interaction.original_response()
    try:
       voice_channel = interaction.user.voice.channel
    except:
        return await msg.edit(content="You're not in a voice channel.")

    if(music.is_connected(interaction=interaction) and music.voice_channel[id].channel.id != voice_channel.id):
        return await msg.edit(content="You must to be in the same voice channel as me in order to execute this command.")
    if not music.is_connected(interaction):
        return await msg.edit(content="I'm not playing songs.")
    
    await music.skip_song(interaction)
#TODO: QUEUE COMMAND
#TODO: STOP COMMAND
