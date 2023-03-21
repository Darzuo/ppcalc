import os
from dotenv import load_dotenv
import info
import helpers


async def help(message, params):
    if len(params) == 0:
        text = info.help
        return await helpers.send_embed(message=message, text=text)
    elif len(params) == 1:
        command = params[0]
        if command in info.commands:
            text = info.instruction_dict[command]
            return await helpers.send_embed(message=message, title=command, text=text)
        else:
            text = f"{command} is not a valid command, type \"!pp help\" for a list of valid commands"
            return await helpers.send_error(message, text)

async def calc(message, params):
     
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")
    
    if len(params) == 1:
        return await helpers.calc(message, "", params[0], 100, -1, api_key)

    elif len(params) == 2:
        return await helpers.calc(message, params[0], params[1], 100, -1, api_key)
    
    elif len(params) == 3:
        return await helpers.calc(message, "", params[0], float(params[1]), int(params[2]), api_key)
    
    elif len(params) == 4:
        return await helpers.calc(message, params[0], params[1], float(params[2]), int(params[3]), api_key)


async def best(message, params):
    load_dotenv()
    api_key = os.getenv("OSU_TOKEN")

    if len(params) == 1:
        username = params[0]
        best = helpers.get_best(api_key=api_key, username=username)
        if len(best) == 0:
            await helpers.send_error(message=message, text=f"{username} is not a valid username or user id, please try again")

        map = helpers.get_map(api_key=api_key, id=best['beatmap_id'])
        
        mod_val = int(best['enabled_mods'])
        mods = helpers.parsemodval(mod_val)
        combo = best['maxcombo']

        title = map['title']
        difficulty = map['version']
        max_combo = map['max_combo']
        acc = str(round(helpers.acc(best)*100, 2))+'%'
        pp = str(round(float(best['pp'])))
        
        beatmapset_id = map['beatmapset_id']
        thumbnail = f'https://b.ppy.sh/thumb/{beatmapset_id}l.jpg'
        
        text=f'*{difficulty}* \n\n\
        Mods: {mods} \n\
        Combo: {combo} / {max_combo} \n\
        Accuracy: {acc} \n\
        pp: {pp}'

        await helpers.send_embed(message=message, title=title, text=text, image=thumbnail)


