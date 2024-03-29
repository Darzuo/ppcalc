
import os
import requests
from dotenv import load_dotenv
import info
from time import sleep

load_dotenv()

token = os.getenv('DISCORD_TOKEN')
api_key = os.getenv("OSU_TOKEN")


url = "https://discord.com/api/v10/applications/1083614941476560966/commands"

headers = {
    "Authorization": f"Bot {token}"
}


commands = [
    {
        "name": "pp",
        "type": 1,
        "description": info.help_info,
        "options": []
    },
    {
        "name": "pphelp",
        "type": 1,
        "description": info.help_info,
        "options": []
    },
    {
        "name": "ppcalc",
        "type": 1,
        "description": info.calc_info,
        "options": [
            {
                "name": "beatmap_link",
                "description": "osu link for the beatmap",
                "type": 3,
                "required": True,
            },
            {
                "name": "mods",
                "description": "mods as a combination of hd hr dt fl (ex. hdhr)",
                "type": 3,
                "required": False,
            },
            {
                "name": "accuracy",
                "description": "accuracy as a number 0-100",
                "type": 10,
                "required": False,
            },
            {
                "name": "max_combo",
                "description": "max combo received",
                "type": 4,
                "required": False
            }
        ]
    },
    {
        "name": "ppbest",
        "type": 1,
        "description": info.best_info,
        "options": [
            {
                "name": "user",
                "description": "osu username or user id",
                "type": 3,
                "required": True
            }
        ]
    },
    {
        "name": "pprec",
        "type": 1,
        "description": info.rec_info,
        "options": [
            {
                "name": "user",
                "description": "osu username or user id",
                "type": 3,
                "required": True
            },
            {
                "name": "mods",
                "description": "mods as a combination of hd hr dt fl (ex. hdhr)",
                "type": 3,
                "required": False
            },
            {
                "name": "max_length",
                "description": "max song length in seconds (min 30s, note that shorter length maps may take longer to find)",
                "type": 4,
                "required": False
            }
        ]
    },
    {
        "name": "ppuser",
        "type": 1,
        "description": info.user_info,
        "options": [
            {
                "name": "user",
                "description": "osu username or user id",
                "type": 3,
                "required": True
            }
        ]
    },
]

for command in commands:
    sleep(0.5)
    r = requests.post(url, headers=headers, json=command)
    print(r)
