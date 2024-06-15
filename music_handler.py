import discord
async def handle_music_events(client):
    
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
    async def add_playlist(interaction:discord.Interaction, voice_channel:discord.VoiceClient, title:str, songs:int):
        msg = await interaction.original_response()
        playlist_embed = discord.Embed(color=discord.Color.yellow())
        playlist_embed.description = f"Added playlist: `{title}` with `{songs}` songs."
        await msg.edit(embed=playlist_embed)
            
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
    @client.music.event
    async def queue_cleared(interaction:discord.Interaction):
        msg = await interaction.original_response()
        q_embed = discord.Embed(color=discord.Color.yellow())
        q_embed.set_author(name='Queue cleared.',icon_url=client.user.display_avatar)
        await msg.edit(embed=q_embed)
