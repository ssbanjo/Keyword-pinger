import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands

import time
from constants import ADMIN_ROLE, BOT_TOKEN, MEMBER_ROLE, PING_POLLING
from helpers import add_ping, check_msg_has_keyword, get_pings, save_pings


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

pings = get_pings()

@client.event
async def on_ready():

    await client.tree.sync()
    
    
@client.event
async def on_message(message: discord.Message):

    if message.author.name != client.user.name:
            
        msg_channel = message.channel.id
        pings_updated = False

        mentions = []
        
        for ping in pings:

            pkws: str = ping["positiveKeywords"]
            nkws: str = ping["negativeKeywords"]
            timestamp: int = ping["pingTimestamp"]
            target = get(message.guild.roles, id=ping["roleId"]) if ping["roleId"] else get(message.guild.members, id=ping["memberId"])
            channel: int = ping["channelId"]

            if msg_channel == channel:

                now = int(time.time())

                if now - timestamp >= PING_POLLING and check_msg_has_keyword(message, pkws, nkws):

                    pings_updated = True

                    ping["pingTimestamp"] = now
                    
                    mentions.append(target.mention)
                    
        if mentions:
            
            await get(message.guild.channels, id=channel).send(" ".join(mentions))

        if pings_updated: save_pings(pings)

    await client.process_commands(message)


@client.tree.command(name="add_ping", description="Add a new role or user based ping.")
@app_commands.checks.has_role(MEMBER_ROLE)
async def add_new_ping(itr: discord.Interaction, target_channel: discord.TextChannel, positive_keywords: str, negative_keywords: str = None, target_role: discord.Role = None):

    global pings

    if target_role and not itr.user.get_role(ADMIN_ROLE):

        await itr.response.send_message("Missing permissions to add role pings")

    else:
        
        if not negative_keywords: 
            
            negative_keywords = []
        
        else:
            
            negative_keywords = negative_keywords.split(",")
            
        positive_keywords = positive_keywords.split(",")
        
        updated_pings = add_ping(target_channel, positive_keywords, negative_keywords, target_role or itr.user)

        pings = updated_pings

        await itr.response.send_message("New ping added successfuly!")

    
async def delete_ping_autocomplete(itr: discord.Interaction, current: str):
    
    data = []
    
    for i, ping in enumerate(pings):
        
        if ping["memberId"] == itr.user.id or itr.user.get_role(ADMIN_ROLE):

            channel: discord.TextChannel = get(itr.guild.channels, id=ping["channelId"])
            target = get(itr.guild.roles, id=ping["roleId"]) if ping["roleId"] else get(itr.guild.members, id=ping["memberId"])
            pkws: list[str] = "/".join(ping["positiveKeywords"])
            nkws: list[str] = "/".join(ping["negativeKeywords"])
            
            if current in (channel.name + target.name + pkws + nkws):
                
                data.append(app_commands.Choice(name=f"#{channel.name} @{target.name} +({pkws}) -({nkws})", value=i))

    return data

@client.tree.command(name="delete_ping", description="Delete a saved ping.")
@app_commands.autocomplete(ping=delete_ping_autocomplete)
@app_commands.checks.has_role(MEMBER_ROLE)
async def delete_ping(itr: discord.Interaction, ping: int):

    global pings
    
    target_ping = pings[ping]
    
    if target_ping["roleId"] and not itr.user.get_role(ADMIN_ROLE):
        
        await itr.response.send_message("Missing permissions to delete role pings")
    
    elif target_ping["memberId"] and (target_ping["memberId"] != itr.user.id) and not itr.user.get_role(ADMIN_ROLE):
        
        await itr.response.send_message("Missing permissions to delete other user pings")
    
    else:
            
        del pings[ping]

        save_pings(pings)

        await itr.response.send_message("Ping deleted successfuly!")


@client.tree.error
async def on_app_command_error(itr: discord.Interaction, error):
    
    if isinstance(error, app_commands.errors.MissingRole): await itr.response.send_message("Missing permissions")

client.run(BOT_TOKEN)