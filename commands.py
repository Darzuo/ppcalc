import os
from dotenv import load_dotenv
import info
import helpers
import numpy as np


async def help(message, params):
    if len(params) == 0:
        text = info.help
        return await helpers.send_embed(interaction=message, text=text)


async def calc(interaction, params):

    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")

    link = params['beatmap_link']
    mods = params['mods'] if 'mods' in params.keys() else ""
    acc = params['accuracy'] if 'accuracy' in params.keys() else 100
    combo = params['max_combo'] if 'max_combo' in params.keys() else -1

    return await helpers.calc(interaction, link, mods, acc, combo, api_key)


async def best(interaction, params):
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")

    user = params['user']
    best = helpers.get_best(api_key=api_key, user=user)
    if len(best) == 0:
        await helpers.send_error(interaction=interaction, text=f"{user} is not a valid username or user id, please try again")

    map = helpers.get_map(api_key=api_key, id=best['beatmap_id'])

    mod_val = int(best['enabled_mods'])
    mods = helpers.parse_mod_val(mod_val)
    combo = best['maxcombo']

    title = map['title']
    difficulty = map['version']
    max_combo = map['max_combo']
    acc = str(round(helpers.acc(best) * 100, 2)) + '%'
    pp = str(round(float(best['pp'])))

    beatmapset_id = map['beatmapset_id']
    thumbnail = f'https://b.ppy.sh/thumb/{beatmapset_id}l.jpg'

    text = f'*{difficulty}* \n\n\
    Mods: {mods} \n\
    Combo: {combo} / {max_combo} \n\
    Accuracy: {acc} \n\
    pp: {pp}'

    await helpers.send_embed(interaction=interaction, title=title, text=text, image=thumbnail)


async def rec(interaction, params):
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")

    user = params['user']
    mods = params['mods'] if 'mods' in params else ""
    max_length = params['max_length'] if 'max_length' in params else np.inf
    if max_length < 30:
        max_length = 30
    acc = round(float(helpers.get_user(api_key=api_key, user=user)['accuracy']), 2)
    mod_val = helpers.parse_mods(mods)

    if mod_val == -1:
        text = f"{mods} is not a valid mod input, mods must be inputted as a combination of hd hr dt fl (ex. hdhr)"
        return await helpers.send_error(interaction, text)

    mods = helpers.parse_mod_val(mod_val)

    scores = helpers.get_scores(api_key=api_key, user=user)

    max_pp = float(scores[0]['pp'])
    min_pp = float(scores[-1]['pp'])

    await interaction.response.defer()

    map_tuple = await helpers.get_map_between(api_key=api_key, min_pp=min_pp, max_pp=max_pp, mod_val=mod_val, acc=acc, max_length=max_length)
    map = map_tuple[0]
    pp = map_tuple[1]

    title = map['title']
    beatmapset_id = map['beatmapset_id']
    beatmap_id = map['beatmap_id']
    thumbnail = f'https://b.ppy.sh/thumb/{beatmapset_id}l.jpg'
    difficulty = map['version']
    max_combo = map['max_combo']

    text = f'*{difficulty}* \n\n\
        Mods: {mods} \n\
        Combo: {max_combo} / {max_combo} \n\
        Accuracy: {acc} \n\
        Estimated pp: {pp} \n\
        https://osu.ppy.sh/beatmapsets/{beatmapset_id}#osu/{beatmap_id}'

    await helpers.followup_send_embed(interaction=interaction, title=title, text=text, image=thumbnail)

commands = {
    "pphelp": help,
    "ppcalc": calc,
    "ppbest": best,
    "pprec": rec
}
