import discord
from urllib import parse, request
import re
import asyncio
from asyncio import run_coroutine_threadsafe
import json
import os
from youtube_dl import YoutubeDL


class Music():
    def __init__(self,client:discord.Client) -> None:
        self.client = client
        self.is_playing = {}
        self.is_paused = {}
        self.queue = {}
        self.queue_index = {}
        self.voice_channel = {}
        self.YTDL_OPTIONS = {'format': 'bestaudio','nonplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    async def initialize(self):
        for guild in self.client.guilds:
            id = guild.id
            self.queue[id] = []
            self.queue_index[id] = 0
            self.voice_channel[id] = None
            self.is_paused[id] = self.is_playing[id] = False
            
    def is_connected(self,interaction):
        voice_client = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        return voice_client is not None
            
    async def join_voice_channel(self,interaction:discord.Interaction, channel:discord.VoiceChannel):
        id = interaction.guild_id
        if self.voice_channel[id] == None or not self.voice_channel[id].is_connected():
            self.voice_channel[id] = await channel.connect()
 
            if self.voice_channel[id] == None:
                raise ConnectionError('Couldn\'t connect to the voice chat.')
        else:
            await self.voice_channel[id].move_to(channel)

    def add_to_queue(self,song,channel=discord.VoiceChannel):
        self.queue[channel.guild.id].append([song, channel])
    
    async def play_music(self, interaction:discord.Interaction,song:str,voice_channel:discord.VoiceChannel):
        id = interaction.guild_id

        if(self.queue_index[id] <= len(self.queue[id])):
            self.is_playing = True
            self.is_paused = False

            await self.join_voice_channel(interaction=interaction,channel=voice_channel)
            search_result = self.search_yt(song)
            song_audio = self.extract_yt(search_result[0])
      
            self.add_to_queue(song_audio, voice_channel)
            print(song_audio['source'])
            self.voice_channel[id].play(discord.FFmpegPCMAudio(source=song_audio['source'], **self.FFMPEG_OPTIONS))
            
    def search_yt(self, search:str):
        query_string = parse.urlencode({'search_query':search})
        htm_content = request.urlopen('https://www.youtube.com/results?'+ query_string)
        search_results = re.findall('/watch\?v=(.{11})', htm_content.read().decode())
        return search_results[:10]
    
    
    
    def extract_yt(self,url:str):
        with YoutubeDL(self.YTDL_OPTIONS) as ydl:
            try:
                info:dict = ydl.extract_info(url, download=False)
            except:
                return False
        return{
            'link': 'https://www.youtube.com/watch?v='+url,
            'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
            'source': info['formats'][0]['url'],
            'title': info['title'],
        } 
        
            
            
    