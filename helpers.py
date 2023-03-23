import discord
import info
import requests
import numpy as np
from joblib import load
from sklearn.preprocessing import PolynomialFeatures
from random import randint

red = info.colors['red']
pink = info.colors['pink']


async def send_error(interaction, text):
    return await send_embed(interaction=interaction, text=text, color='red', title="Error")


async def send_embed(interaction, text, color='pink', title="", thumbnail=None, image=None):
    embed = discord.Embed(title=title, color=info.colors[color], description=text)
    if image is not None:
        embed.set_image(url=image)
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    return await interaction.response.send_message(embed=embed)


async def followup_send_embed(interaction, text, color='pink', title="", thumbnail=None, image=None):
    embed = discord.Embed(title=title, color=info.colors[color], description=text)
    if image is not None:
        embed.set_image(url=image)
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    return await interaction.followup.send(embed=embed)


async def calc(interaction, link, mods, acc, combo, api_key):

    if 'osu.ppy.sh' not in link:
        text = f'"{link}" is not a valid osu beatmap link, please try again'
        return await send_error(interaction, text)

    id = int(link.split('/')[-1])

    map = get_map(api_key=api_key, id=id)
    if combo == -1:
        combo = int(map['max_combo'])

    mod_val = parse_mods(mods)
    if mod_val == -1:
        text = f"{mods} is not a valid mod input, mods must be inputted as a combination of hd hr dt fl (ex. hdhr)"
        return await send_error(interaction, text)
    prediction = predict(map, acc, combo, mod_val)

    text = f"Estimated pp: {prediction}"

    return await send_embed(interaction=interaction, text=text)


def parse_mods(mods):
    mod_dict = {"hd": 8, "dt": 64, "hr": 16, "fl": 1024}

    if mods.replace("*", "") == "":
        return 0
    if len(mods.replace("*", "")) <= 1:
        return -1

    for mod in mod_dict.keys():
        if mod in mods:
            parsed_val = parse_mods(mods.replace(mod, "*"))
            if parsed_val == -1:
                return -1
            return mod_dict[mod] + parsed_val
    return -1


def parse_mod_val(mod_val):
    if mod_val == 0:
        return "None"
    mods = ""
    if (mod_val & 1 << 3):
        mods += "HD, "
    if (mod_val & 1 << 4):
        mods += "HR, "
    if (mod_val & 1 << 9):
        mods += "NC, "
    if (mod_val & 1 << 6):
        mods += "DT, "
    if (mod_val & 1 << 10):
        mods += "FL, "

    return mods[:-2]


def predict(map, acc, combo, mod_val):
    model = load(f"models/model{mod_val}.joblib")
    polys = load("models/model_info")

    data = [float(map['diff_overall']),
            float(map['diff_approach']),
            float(map['diff_aim']),
            float(map['diff_speed']),
            float(map['difficultyrating']),
            float(map['bpm']),
            float(map['max_combo']),
            float(acc / 100),
            float(int(map['max_combo']) - combo) / float(combo)]

    X = np.asarray(data).reshape(-1, len(data))
    if (mod_val) in polys:
        poly_feats = PolynomialFeatures(degree=2)
        X = poly_feats.fit_transform(X)

    pred = np.exp(model.predict(X))[0]

    return int(pred)


def acc(score):
    perf = int(score['count300']) + int(score['countgeki'])
    mid = int(score['count100']) + int(score['countkatu'])
    low = int(score['count50'])
    miss = int(score['countmiss'])
    total = perf + mid + low + miss
    acc = float(300 * perf + 100 * mid + 50 * low) / (300 * total)
    return acc


def parse_params(params):
    out = {}
    for param in params:
        out[param['name']] = param['value']
    return out


def get_best(api_key, user):

    params = {"k": api_key,
              "u": user,
              "m": 0,
              "limit": 1}
    best = requests.get("https://osu.ppy.sh/api/get_user_best", params=params).json()
    if len(best) == 0:
        return best
    return best[0]


def get_map(api_key, id):

    params = {"k": api_key,
              "m": 0,
              "b": id}

    map = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=params).json()[0]
    return map


def get_scores(api_key, user):

    params = {"k": api_key,
              "u": user,
              "m": 0,
              "limit": 25}

    scores = requests.get("https://osu.ppy.sh/api/get_user_best", params=params).json()
    return scores


def get_user(api_key, user):

    params = {"k": api_key,
              "u": user,
              "m": 0}

    user = requests.get("https://osu.ppy.sh/api/get_user", params=params).json()[0]
    return user


async def get_map_between(api_key, min_pp, max_pp, mod_val, acc, max_length):

    count = 0

    while True:

        year = randint(2010, 2022)
        month = randint(1, 12)
        day = randint(1, 28)
        if month < 10:
            month = '0' + str(month)
        if day < 10:
            day = '0' + str(day)
        start_date = f'{year}-{month}-{day}'

        params = {"k": api_key,
                  "m": 0,
                  "since": start_date}

        beatmaps = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=params).json()

        for map in beatmaps:
            if map["approved"] != '1' or int(map['total_length']) > max_length:
                continue
            combo = int(map['max_combo'])
            prediction = predict(map, acc, combo, mod_val)

            if prediction > min_pp and prediction < max_pp:
                return (map, prediction)

        count += 500
        print(f"processed {count} beatmaps")
