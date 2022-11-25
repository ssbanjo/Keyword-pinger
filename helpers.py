import json
import discord

from constants import SETTINGS_PATH

def get_pings() -> list:

    with open(SETTINGS_PATH, "r") as f:

        return json.loads(f.read())

def save_pings(new_pings: list):

    with open(SETTINGS_PATH, "w") as f:

        f.write(json.dumps(new_pings, indent=3))

def add_ping(channel: discord.TextChannel, keyword: str, role: discord.Role) -> list:

    pings = get_pings()
    
    pings.append(
        {
            "channel": channel.id,
            "keyword": keyword,
            "role": role.id,
            "timestamp": 0
        }
    )

    save_pings(pings)

    return pings

def check_msg_has_keyword(msg: discord.Message, keyword: str) -> bool:

    keyword = keyword.lower()

    if keyword in msg.content: return True

    for embed in msg.embeds:

        if embed.title and keyword in embed.title: return True
        if embed.description and keyword in embed.description: return True
        if embed.url and keyword in embed.url: return True

        if any(keyword in field.value for field in embed.fields if field.value): return True

    return False

