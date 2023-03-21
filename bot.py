# discord bot integration

import os
import discord
from dotenv import load_dotenv
import info
import commands
import helpers

load_dotenv()

client = discord.Client()
token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv("OSU_TOKEN")

@client.event
async def on_ready():
    print(f"{client.user} connected!")
    
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
  
    if channel == "bot" or "jukebox-jumbo":
        if user_message.startswith("!pp"):
            await handle_command(message, user_message)
        
async def handle_command(message, user_message):
    if user_message == "!pp":
        await commands.help(message, [])
    else:
        parsed = user_message.split(' ')
        if len(parsed) <= 1:
            return # invalid !ppxxxx command
        command = parsed[1:]
        command_name = command[0]
        params = command[1:]

        if command_name not in info.commands:
            text = f"{command} is not a valid command, type \"!pp help\" for a list of valid commands"
            return await helpers.send_error(message, text)
        if (len(params) not in info.param_nums[command_name]):
            text = f'Invalid command, see usage:\n{info.instruction_dict[command_name]}'
            return await helpers.send_error(message, text)
        
        if (command_name == 'help'):
            await commands.help(message, params)
        elif (command_name == 'calc'):
            await commands.calc(message, params)
        elif (command_name == 'best'):
            await commands.best(message, params)

client.run(token)