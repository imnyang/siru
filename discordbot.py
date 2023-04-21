import discord, asyncio, PingPongWr
import os, random
import requests, json
from datetime import datetime, timezone, timedelta
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv
load_dotenv()

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

PREFIX = os.environ['PREFIX']
client = discord.Client(intents=discord.Intents.all())

url = os.environ['PINGPONG_URL']  # 핑퐁빌더 Custom API URL
pingpong_token = os.environ['PINGPONG_TOKEN']  # 핑퐁빌더 Custom API Token

Ping = PingPongWr.Connect(url, pingpong_token)  # 핑퐁 모듈 클래스 선언

def get_weather_today():
    city = "Seoul" #도시
    apiKey = os.environ['WEATHER_API_KEY'] #OpenWeather API Key
    lang = 'kr' #언어
    units = 'metric' #화씨 온도를 섭씨 온도로 변경
    api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&lang={lang}&units={units}"

    result = requests.get(api)
    result = json.loads(result.text)

    name = result['name']
    lon = result['coord']['lon']
    lat = result['coord']['lat']
    weather = result['weather'][0]['main']
    temperature = result['main']['temp']
    humidity = result['main']['humidity']
    return name, lon, lat, weather, temperature, humidity

def store_data(id, text, return_data):
    KST = timezone(timedelta(hours=9))
    time_record = datetime.now(KST)
    time_record_str = time_record.strftime('%Y%m%d-%H%M%S')
    print(time_record_str)
    doc_ref = db.collection(u'logs').document(time_record_str)
    doc_ref.set({
        u'userid': id,
        u'time': time_record,
        u'ask': text,
        u'reply': return_data
    })

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"{PREFIX} 오늘 날씨 어때?"):
        weather = get_weather_today()

        disembed=discord.Embed(title="오늘의 날씨", description="날씨는 서울시 기준입니다.", color=0xffffff)
        disembed.add_field(name="날씨", value=weather[3], inline=False)
        disembed.add_field(name="온도", value=f"{weather[2]}ºC", inline=False)
        disembed.add_field(name="습도", value=f"{weather[4]}%", inline=False)
        await message.channel.send(embed=disembed)

    else:
        if message.content.startswith(f"{PREFIX} "):
            str_text = (message.content.split(" "))[1].replace(f'{PREFIX} ', '')
            async with message.channel.typing():
                type_time = random.uniform(0.5, 2)
                await asyncio.sleep(type_time)
            
            return_data = await Ping.Pong(session_id ="Example", text = str_text, topic = True, image = True, dialog = True) # 핑퐁빌더 API에 Post 요청
            id = message.author.id
            store_data(id, str_text, return_data["text"])
            await message.reply(return_data["text"], mention_author=False)
        
        elif message.content.startswith(f"{PREFIX}"):
            async with message.channel.typing():
                type_time = random.uniform(0.5, 2)
                await asyncio.sleep(type_time)
                
            return_data = await Ping.Pong(session_id ="Example", text = PREFIX, topic = True, image = False, dialog = True) # 핑퐁빌더 API에 Post 요청
            await message.reply(return_data["text"], mention_author=False)


client.run(os.environ['DISCORD_TOKEN'])

