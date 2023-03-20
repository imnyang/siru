import discord
import PingPongWr
import os

from discord.ext import commands

bot = commands.Bot(command_prefix='시루야 ')

url = os.environ['PINGPONG_URL']  # 핑퐁빌더 Custom API URL
pingpong_token = os.environ['PINGPONG_TOKEN']  # 핑퐁빌더 Custom API Token

Ping = PingPongWr.Connect(url, pingpong_token)  # 핑퐁 모듈 클래스 선언

@bot.event()
async def on_message(message):

    if message.author == bot.user:
            return

    if message.content.startswith("시루야"):
        str_text = (message.content.split(" "))[1].replace('시루야 ', '')
        return_data = await Ping.Pong(session_id ="Example", text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
        await message.channel.reply(return_data["text"])

bot.run(os.environ['DISCORD_TOKEN'])
