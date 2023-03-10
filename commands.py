import os
from dotenv import load_dotenv
from joblib import load
import requests
import numpy as np
import info

async def help(message, params):
    if len(params) == 0:
            await message.channel.send(info.help)
    elif len(params) == 1:
        if params[0] in info.commands:
            await message.channel.send(info.instruction_dict[params[0]])
    else:
        await message.channel.send(f'Invalid command, see usage:\n{info.help_instr}')


async def calc(message, params):
     
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")
    
    if len(params) == 1:
        
        link = params[0]
        id = int(link.split('/')[-1])
        map = request(api_key, id)

        acc = 100.
        combo = int(map['max_combo'])

        prediction = predict(map, acc, combo)
        await message.channel.send(f"Estimated pp: {prediction}")
    
    elif len(params) == 3:

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