# discord bot integration

import os
import discord
from dotenv import load_dotenv
from joblib import load
import requests
import numpy as np
import info


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
        if user_message.startswith("!pp"):
            return await handle_command(message, user_message)

        params = user_message.split(" ")
        prediction = predict(api_key, int(params[0]), float(params[1]), int(params[2]))
        await message.channel.send(prediction)


async def handle_command(message, user_message):
    if (user_message == "!pp"):
        return await message.channel.send(info.help)
    command = user_message.split(' ')[1:]
    command_name = command[0]
    params = command[1:]
    num_params = len(params)
    
    if (command_name == 'help'):
        if num_params == 0:
            return await message.channel.send(info.help)
        if num_params == 1:
            if params[0] in info.commands:
                return await message.channel.send(info.instruction_dict[params[0]])
        else:
            return await message.channel.send(f'Invalid command, see usage:\n{info.help_instr}')
    elif (command_name == 'calc'):
        if num_params == 1:
            
            link = params[0]
            id = int(link.split('/')[-1])
            map = request(api_key, id)

            acc = 100.
            combo = int(map['max_combo'])

            prediction = predict(map, acc, combo)
            return await message.channel.send(f"Estimated pp: {prediction}")
        
        if num_params == 3:

            link = params[0]
            id = int(link.split('/')[-1])
            map = request(api_key=api_key)
            
            acc = float(params[1])
            combo = int(params[2])


            prediction = predict(map, acc, combo)
            return await message.channel.send(f"Estimated pp: {prediction}")
        
        else:
            return await message.channel.send(f'Invalid command, see usage:\n{info.calc_instr}')

def request(api_key, id):

    params = {"k": api_key,
        "m": 0,
        "b": id}
    
    map = requests.get(f"https://osu.ppy.sh/api/get_beatmaps", params=params).json()[0]
    return map

def predict(map, acc, combo):
    linreg = load("models/linreg_full.joblib")

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