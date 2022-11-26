import json
import discord

def get_pings() -> list:

    with open("pings.json", "r") as f:

        return json.loads(f.read())

def save_pings(new_pings: list):

    with open("pings.json", "w") as f:

        f.write(json.dumps(new_pings, indent=3))

def add_ping(channel: discord.TextChannel, keyword: str, role: discord.Role) -> list:

    pings = get_pings()
    
    pings.append(
        {
            "channelId": channel.id,
            "keyword": keyword,
            "roleId": role.id,
            "pingTimestamp": 0
        }
    )

    save_pings(pings)

    return pings

def check_msg_has_keyword(msg: discord.Message, keyword: str) -> bool:

    keyword = keyword.lower()

    if keyword in msg.content.lower(): return True

    for embed in msg.embeds:

        if embed.title and keyword in embed.title.lower(): return True
        if embed.description and keyword in embed.description.lower(): return True
        if embed.url and keyword in embed.url.lower(): return True

        if any(keyword in field.value.lower() for field in embed.fields if field.value): return True

    return False

