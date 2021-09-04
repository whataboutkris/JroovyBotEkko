"""
push and pull test
Boilerplate taken from
https://realpython.com/how-to-make-a-discord-bot-python/#what-is-a-bot
"""
#bot.py
import os
import discord
from discord.ext.commands.core import guild_only
import youtube_dl
import asyncio
from discord.ext import commands, tasks

from random import choice

##########################################################

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

##########################################################




client = commands.Bot(command_prefix = '-')

status = ['with your mom!', 'with my balls!', 'to friends!']




@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} has connected to Discord!')



@client.command(name = 'play', help = 'how2play')
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send("bruh get in the call")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()
    


@client.command(name = 'stop', help = 'how2stop')
async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect() 



@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command() 
async def hello(ctx):
    await ctx.send('World!')


@tasks.loop(seconds=4)    #just for lols
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

client.run('ODgzMTM5NDEwMDc2NTA4MjUx.YTFlqw.kNkUvlQ8t7-HEcJzMiomm5zjPug')