from discord import app_commands, Interaction
import discord
from music import Music

@app_commands.describe(song='The song title.')
async def play_command(interaction: Interaction, song:str):
    client = interaction.client
    music:Music = client.music
    
    await interaction.response.defer()
    msg = await interaction.original_response()
    try:
       voice_channel = interaction.user.voice.channel
    except:
        return await msg.edit(content="You're not in a voice channel.")
    
    
    if(music.is_connected(interaction=interaction)):
        return await msg.edit(content="I'm already connected in another channel.")
    
    await music.play_music(interaction=interaction,song=song,voice_channel=voice_channel)
    await msg.edit(content="connected")