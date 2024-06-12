import discord
from urllib import parse, request, error
import re
from youtube_dl import YoutubeDL
from typing import Callable, Any
import asyncio
import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)

#TODO: ADD STOP FUNCTION
#TODO: ADD YT PLAYLIST SUPPORT
#TODO: ADD SPOTIFY PLAYLIST AND LINK SUPPORT


class Music:
    def __init__(self, client: discord.Client) -> None:
        self.callbacks = {}
        self.client = client
        self.is_playing = {}
        self.is_paused = {}
        self.queue = {}
        self.queue_index = {}
        self.voice_channel = {}
        self.YTDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

    async def initialize(self):
        for guild in self.client.guilds:
            id = guild.id
            self.queue[id] = []
            self.queue_index[id] = 0
            self.voice_channel[id] = None
            self.is_paused[id] = self.is_playing[id] = False

    def event(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.callbacks[func.__name__] = func
        return func        

    async def call_event(self, event_name: str, *args, **kwargs):
        if event_name in self.callbacks:
            await self.callbacks[event_name](*args, **kwargs)

    def is_connected(self, interaction):
        voice_client = discord.utils.get(self.client.voice_clients, guild=interaction.guild)
        return voice_client is not None

    async def join_voice_channel(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        id = interaction.guild_id
        if self.voice_channel[id] is None or not self.voice_channel[id].is_connected():
            self.voice_channel[id] = await channel.connect()

            if self.voice_channel[id] is None:
                return await self.call_event('music_error', interaction, 'connection')
        else:
            await self.voice_channel[id].move_to(channel)

    async def add_to_queue(self, song_audio, interaction: discord.Interaction):
        id = interaction.guild.id
        self.queue[id].append([song_audio])
        await self.call_event('add_song', interaction, self.voice_channel[id], song_audio)

    async def play_music(self, interaction: discord.Interaction, song: str, voice_channel: discord.VoiceChannel):
        id = interaction.guild_id
        try:
            search_result = self.search_yt(song)
            song_audio = self.extract_yt(search_result[0])
            if not song_audio or not self.verify_url(song_audio['source']):
                return await self.call_event('music_error', interaction, 'download')
        except Exception as e:
            return await self.call_event('music_error', interaction, 'download')

        await self.add_to_queue(song_audio=song_audio, interaction=interaction)

        if not self.is_playing[id]:
            self.is_playing[id] = True
            self.is_paused[id] = False

            await self.join_voice_channel(interaction=interaction, channel=voice_channel)

            try:
                self.voice_channel[id].play(
                    discord.FFmpegPCMAudio(source=song_audio['source'], **self.FFMPEG_OPTIONS),
                    after=lambda e: self.handle_playback_error(interaction, e)
                )
                await self.call_event('play_song', interaction, self.voice_channel[id], song_audio, False)
            except Exception as e:
                await self.call_event('music_error', interaction, 'playback')

    def handle_playback_error(self, interaction: discord.Interaction, error: Exception):
        if error:
            logging.error(f"Playback error: {error}")
        self.play_next(interaction)

    def play_next(self, interaction: discord.Interaction):
        id = interaction.guild_id
        if not self.is_playing[id]:
            return

        self.queue_index[id] += 1

        if self.queue_index[id] < len(self.queue[id]):
            song = self.queue[id][self.queue_index[id]][0]
            if self.verify_url(song['source']):
                self.voice_channel[id].play(
                    discord.FFmpegPCMAudio(source=song['source'], **self.FFMPEG_OPTIONS),
                    after=lambda e: self.handle_playback_error(interaction, e)
                )
                coro = self.call_event('play_song', interaction, self.voice_channel[id], song, True)
                asyncio.run_coroutine_threadsafe(coro, self.client.loop)
            else:
                # Try to regenerate the URL and play again
                new_song_audio = self.extract_yt(song['link'])
                if new_song_audio and self.verify_url(new_song_audio['source']):
                    self.voice_channel[id].play(
                        discord.FFmpegPCMAudio(source=new_song_audio['source'], **self.FFMPEG_OPTIONS),
                        after=lambda e: self.handle_playback_error(interaction, e)
                    )
                    coro = self.call_event('play_song', interaction, self.voice_channel[id], new_song_audio, True)
                    asyncio.run_coroutine_threadsafe(coro, self.client.loop)
                else:
                    self.play_next(interaction)
        else:
            self.is_playing[id] = False

    async def get_queue(self, interaction: discord.Interaction):
        id = interaction.guild_id
        if self.queue[id]:
            queue_list = []
            for index, song_info in enumerate(self.queue[id]):
                if index == 0:
                    song_dict = {
                        'title': song_info[0]['title'],
                        'link': song_info[0]['link'],
                        'duration': song_info[0]['duration'],
                        'thumbnail': song_info[0]['thumbnail']
                    }
                else:
                    song_dict = {
                        'title': song_info[0]['title'],
                        'link': song_info[0]['link'],
                        'duration': song_info[0]['duration']
                    }
                queue_list.append(song_dict)
            return queue_list
        else:
            return False

    async def skip_song(self, interaction: discord.Interaction):
        id = interaction.guild_id
        if self.is_playing[id] and self.voice_channel[id]:
            voice: discord.VoiceClient = self.voice_channel[id]
            voice.stop()

            # Verificar si hay una canción en la cola para reproducir
            if self.queue_index[id] + 1 < len(self.queue[id]):
                await self.call_event('song_skipped', interaction, True)
                self.play_next(interaction)
            else:
                await voice.disconnect()
                self.is_playing[id] = False
                self.is_paused[id] = False
                await self.call_event('song_skipped', interaction, False)
        else:
            # Si no hay canción en reproducción, simplemente desconectarse
            if self.voice_channel[id]:
                voice: discord.VoiceClient = self.voice_channel[id]
                await voice.disconnect()
            self.is_playing[id] = False
            self.is_paused[id] = False
            await self.call_event('song_skipped', interaction, False)

    def search_yt(self, search: str):
        query_string = parse.urlencode({'search_query': search})
        htm_content = request.urlopen('https://www.youtube.com/results?' + query_string)
        search_results = re.findall('/watch\?v=(.{11})', htm_content.read().decode())
        return search_results[:10]

    def extract_yt(self,url: str):
        retries = 0
        while retries < 10:
            with YoutubeDL(self.YTDL_OPTIONS) as ydl:
                try:
                    info: dict = ydl.extract_info(url, download=False)
                    formatted_info = {
                        'link': 'https://www.youtube.com/watch?v=' + url,
                        'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg',
                        'source': info['formats'][0]['url'],
                        'title': info['title'],
                        'channel': info['channel'],
                        'channel_url': info['channel_url'],
                        'duration': str(datetime.timedelta(seconds=info['duration']))
                    }
                    if self.verify_url(formatted_info['source']):
                        return formatted_info
                except Exception as e:
                    return

            retries += 1
        return False


    def verify_url(self, url):
        try:
            response = request.urlopen(url)
            return response.status == 200
        except error.HTTPError as e:
            return False
        except Exception as e:
            return False
