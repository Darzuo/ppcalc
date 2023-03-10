# discord bot integration

import os
import discord
from dotenv import load_dotenv
from joblib import load
import requests
import numpy as np


load_dotenv()

client = discord.Client()
token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv("OSU_TOKEN")

print(type(token))

@client.event
async def on_ready():
    print(f"{client.user} connected!")

    
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
  
    print(f'Message {user_message} by {username} on {channel}')
  
  
    if channel == "bot" or "jukebox-jumbo":
        params = user_message.split(' ')
        prediction = predict(api_key, int(params[0]), float(params[1]), int(params[2]))
        await message.channel.send(prediction)
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
            
def predict(api_key, id, acc, combo):
    linreg = load("models/linreg_full.joblib")

    params = {"k": api_key,
        "m": 0,
        "b": id}

    map = requests.get(f"https://osu.ppy.sh/api/get_beatmaps", params=params).json()[0]

    data = [float(map['diff_overall']),
            float(map['diff_approach']),
            float(map['diff_aim']),
            float(map['diff_speed']),
            float(map['difficultyrating']),
            float(map['bpm']),
            float(map['max_combo']),
            float(acc/100),
            float(int(map['max_combo'])-combo)/float(combo)]

    X = np.asarray(data).reshape(-1, len(data))

    pred = np.exp(linreg.predict(X))[0]

    return int(pred)




client.run(token)