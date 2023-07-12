import json
import string
from typing import Union
import discord

def get_pings() -> list:

    with open("pings.json", "r") as f:

        return json.loads(f.read())

def save_pings(new_pings: list):

    with open("pings.json", "w") as f:

        f.write(json.dumps(new_pings, indent=3))

def add_ping(channel: discord.TextChannel, positive_keywords: list[str], negative_keywords: list[str], target: Union[discord.Role, discord.Member]) -> list:

    pings = get_pings()
    
    pings.append(
        {
            "channelId": channel.id,
            "positiveKeywords": positive_keywords,
            "negativeKeywords": negative_keywords,
            "roleId": target.id if isinstance(target, discord.Role) else None,
            "memberId": target.id if isinstance(target, discord.Member) else None,
            "pingTimestamp": 0
        }
    )

    save_pings(pings)

    return pings

def check_msg_has_keyword(msg: discord.Message, positive_keywords: list[str], negative_keywords: list[str]) -> bool:

    positive_keywords = [k.lower() for k in positive_keywords]
    negative_keywords = [k.lower() for k in negative_keywords]

    txt = _parse_msg_text(msg).lower()

    return all(k in txt for k in positive_keywords) and all(k not in txt for k in negative_keywords)


def _parse_msg_text(msg: discord.Message) -> str:
    
    txt = msg.content
    
    for embed in msg.embeds:
        
        if embed.title: txt += embed.title
        if embed.description: txt += embed.description
        if embed.url: txt += embed.url

        for field in embed.fields:
            
            if field.value: txt += field.value
    
    return txt