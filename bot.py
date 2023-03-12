# discord bot integration

import os
import discord
from dotenv import load_dotenv
import info
import commands


load_dotenv()

client = discord.Client()
token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv("OSU_TOKEN")

pink = info.colors['osu_pink']


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
        text = info.help
        await message.channel.send(embed=discord.Embed(title='PPCalc', color = pink, description = text))
    else:
        parsed = user_message.split(' ')
        if len(parsed) <= 1:
            return # invalid !ppxxxx command
        command = parsed[1:]
        command_name = command[0]
        params = command[1:]
        
        if (command_name == 'help'):
            await commands.help(message, params)
        elif (command_name == 'calc'):
            await commands.calc(message, params)

client.run(token)