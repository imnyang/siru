from cmath import log
from distutils.sysconfig import PREFIX
import discord
import PingPongWr
import os
import random
import asyncio
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

PREFIX = "시루야"

client = discord.Client(intents=discord.Intents.all())

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

    if message.content.startswith("세아라 "):
        
        async with message.channel.typing():
            type_time = random.uniform(0.5, 2)
            await asyncio.sleep(type_time)
        
        str_text = (message.content.split(" "))[1].replace('세아라 ', '')
        return_data = await Ping.Pong(session_id ="Example", text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
        KST = timezone(timedelta(hours=9))
        time_record = datetime.now(KST)
        time_record_str = time_record.strftime('%Y%m%d-%H%M%S')
        print(time_record_str)
        doc_ref = db.collection(u'logs').document(time_record_str)
        doc_ref.set({
            u'userid': message.author.id,
            u'time': time_record,
            u'ask': str_text,
            u'reply': return_data["text"]
        })
        await message.reply(return_data["text"], mention_author=False)

    elif message.content.startswith("시루야"):
        async with message.channel.typing():
            type_time = random.uniform(0.5, 2)
            await asyncio.sleep(type_time)
            
        str_text = "시루야"
        return_data = await Ping.Pong(session_id ="Example", text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
        await message.reply(return_data["text"], mention_author=False)


client.run(os.environ['DISCORD_TOKEN'])

