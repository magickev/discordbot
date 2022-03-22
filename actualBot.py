from __future__ import unicode_literals
from pytube import YouTube
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from moviepy.editor import *
import time
from pathlib import Path


def removeFiles():
    directory = os.getcwd()
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if (file.endswith(".part") or file.endswith(".mp3") or file.endswith(".mp4"))]

    for file in filtered_files:
        try:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        except:
            directory = os.getcwd()


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# def my_hook(d):
#    if d['status'] == 'finished':
#        print('Done downloading, now converting ...')
#
# ydl_opts = {
#    'format': 'bestaudio/best',
#    'postprocessors': [{
#        'key': 'FFmpegExtractAudio',
#        'preferredcodec': 'mp3',
#        'preferredquality': '192',
#    }],
#    'logger': MyLogger(),
#    'progress_hooks': [my_hook],
#	'outtmpl': './1.mp3'
# }

def dl_vid(url):
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

    time.sleep(1)
    directory = os.getcwd()
    paths = sorted(Path(directory).iterdir(), key=os.path.getmtime)
    filtered_path = [files for files in paths if (str(files)).endswith(".mp4")]

    #files_in_directory = os.listdir(directory)
    #filtered_files = [file for file in files_in_directory if file.endswith(".mp4")]
    
    

    video = VideoFileClip(os.path.join(directory, filtered_path[len(filtered_path) - 1]))
    video.audio.write_audiofile(os.path.join("1.mp3"))


# YouTube(url).streams.first().download()
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#	result = ydl.download([url])

# 1
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

players = {}

# 2
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(pass_context=True)
async def nc(ctx, url, ear="loud", speed=1.5, vol="150"):
    filename = '2.mp3'

    if len(players) > 0:
        players[0].stop()
    else:
        try:
            players[0].stop()
        except:
            print("waht the")

    time.sleep(1)
    removeFiles()
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("You are not connected to a voice channel")
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    dl_vid(url)
    os.system("ffmpeg -i 1.mp3 -af asetrate=44100*" + str(speed) + ",aresample=44100 2.mp3")

    if ear == "loud":
        os.system("ffmpeg -i 2.mp3 -filter:a \"volume=" + vol + "\" 3.mp3")
        filename = '3.mp3'

    source = FFmpegPCMAudio(filename)
    player = voice.play(source)

    players[0] = voice


@bot.command(pass_context=True)
async def clear(ctx):
    try:
        os.remove("1.mp3")
    except:
        print("test")
    try:
        os.remove("2.mp3")
    except:
        print("test")


bot.run(TOKEN)

