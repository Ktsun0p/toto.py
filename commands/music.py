from discord import app_commands, Interaction
import discord
from music import Music
#TODO: COMPLETAR MUSIC.PY
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
    
async def autoplay_command(interaction:Interaction):
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
    music.autoplay[id] = not music.autoplay[id]
    status = 'Enabled' if music.autoplay[id] else 'disabled'
    await msg.edit(content=f'Autplay has been {status}')
    
async def queue_command(interaction:Interaction):
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
        return await msg.edit(content="Queue is empty.")
    
    queue = await music.get_queue(interaction=interaction)
    autoplay = 'enabled' if music.autoplay[id] else 'disabled'
    loop = 'enabled' if music.loop[id] else 'disabled'
    queue_list = []
    for i,song in enumerate(queue):
        formatted_song = f'**`{i+1}`**. [`{song['title']}`]({song['link']})'
        queue_list.append(formatted_song)
        
    embed = discord.Embed(color=discord.Color.yellow())
    embed.set_thumbnail(url=queue[0]['thumbnail'])
    embed.set_author(name=client.user.display_name,icon_url=client.user.display_avatar)
    embed.title = f'🎵 {interaction.guild.name}\'s queue. 🎵'    
    embed.description = "\n".join(queue_list)
    embed.add_field(name='Options',value=f'Loop: **{loop}**. Autoplay: **{autoplay}**.')
     
    return await msg.edit(embed=embed)

async def clear_command(interaction:Interaction):
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
        return await msg.edit(content="The queue is already empty.")
    
    await music.clear_queue(interaction=interaction)

#TODO: Clear command
#TODO: Pause command
#TODO: Resume command