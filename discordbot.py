from cmath import log
from distutils.sysconfig import PREFIX
import discord
import PingPongWr
import os

PREFIX = "시루야"

client = discord.Client()

url = os.environ['PINGPONG_URL']  # 핑퐁빌더 Custom API URL
pingpong_token = os.environ['PINGPONG_TOKEN']  # 핑퐁빌더 Custom API Token

Ping = PingPongWr.Connect(url, pingpong_token)  # 핑퐁 모듈 클래스 선언

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("시루야"):
        str_text = (message.content.split(" "))[1].replace('시루야 ', '')
        return_data = await Ping.Pong(session_id ="Example", text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
        await message.channel.reply(return_data["text"])


try:
    client.run(os.environ['DISCORD_TOKEN'])
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
