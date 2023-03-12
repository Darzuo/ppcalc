import os
from dotenv import load_dotenv
from joblib import load
import requests
import numpy as np
import info
import discord

pink = info.colors['osu_pink']
red = info.colors['error_red']

async def help(message, params):
    if len(params) == 0:
        text = info.help
        return await __send_embed(message, 'PPCalc', pink, text)
    elif len(params) == 1:
        command = params[0]
        if command in info.commands:
            text = info.instruction_dict[command]
            return await __send_embed(message, 'PPCalc', pink, text)
        else:
            text = f"{command} is not a valid command, type \"!pp help\" for a list of valid commands"
            return await __send_error(message, text)
    else:
        text = f'Invalid command, see usage:\n{info.help_instr}'
        return await __send_error(message, text)

async def calc(message, params):
     
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")
    
    if len(params) == 1:
        return await __calc(message, "", params[0], 100, -1, api_key)

    if len(params) == 2:
        return await __calc(message, params[0], params[1], 100, -1, api_key)
    
    elif len(params) == 3:
        return await __calc(message, "", params[0], float(params[1]), int(params[2]), api_key)
    
    elif len(params) == 4:
        return await __calc(message, params[0], params[1], float(params[2]), int(params[3]), api_key)

    else:
        text = f'Invalid command, see usage:\n{info.calc_instr}'
        return await __send_error(message, text)

async def __calc(message, mods, link, acc, combo, api_key):
    
    if 'osu.ppy.sh' not in link:
        text = f'"{link}" is not a valid osu beatmap link, please try again'
        return await __send_error(message, text)
    
    id = int(link.split('/')[-1])

    map = __get_map(api_key=api_key, id=id)
    if combo == -1:
        combo = int(map['max_combo'])

    mod_val = __parsemods(mods)
    if mod_val == -1:
        text = f"{mods} is not a valid mod input, see usage:\n{info.calc_instr}"
        return await __send_error(message, text)
    if mod_val != 0 and mod_val != 8:
        text = f"placeholder: prediction with mod_val {mod_val}"
        return await __send_embed(message, "", pink, text)
    prediction = __predict(map, acc, combo, mod_val)
    text = f"Estimated pp: {prediction}"
    return await __send_embed(message, "", pink, text)



async def __send_error(message, text):
    return await message.channel.send(embed=discord.Embed(title='Error', color=red, description=text))

async def __send_embed(message, title, color, text):
    return await message.channel.send(embed=discord.Embed(title=title, color=color, description=text))

def __parsemods(mods):
    mod_dict = {"hd": 8, "dt": 64, "hr": 16, "fl": 1024}

    if mods.replace("*","") == "":
        return 0
    if len(mods.replace("*","")) <= 1:
        return -1
    
    for mod in mod_dict.keys():
        if mod in mods:
            parsed_val = __parsemods(mods.replace(mod,"*"))
            if parsed_val == -1:
                return -1
            return mod_dict[mod] + parsed_val
    
    return -1


def __get_map(api_key, id):

    params = {"k": api_key,
              "m": 0,
              "b": id}
    
    map = requests.get(f"https://osu.ppy.sh/api/get_beatmaps", params=params).json()[0]
    return map

def __predict(map, acc, combo, mod_val):
    linreg = load(f"models/linreg{mod_val}.joblib")

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