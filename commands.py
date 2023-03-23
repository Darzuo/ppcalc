import os
from dotenv import load_dotenv
import info
import helpers


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
    mods = helpers.parsemodval(mod_val)
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

commands = {
    "pphelp": help,
    "ppcalc": calc,
    "ppbest": best
}
