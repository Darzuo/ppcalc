# discord bot integration

import os
import discord
from dotenv import load_dotenv
import commands
import helpers

load_dotenv()

client = discord.Client()
token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv("OSU_TOKEN")


@client.event
async def on_interaction(interaction):
    if str(interaction.type) == "InteractionType.application_command":
        command_name = interaction.data['name']
        options = interaction.data['options'] if 'options' in interaction.data else []
        params = helpers.parse_params(options)
        await commands.commands[command_name](interaction, params)


@client.event
async def on_ready():
    print(f"{client.user} connected!")

client.run(token)
