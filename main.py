import discord
from discord.ext import commands
from discord.utils import get
from dhooks import Embed
import time
from constants import COMMAND_PREFIX, BOT_TOKEN, COMMANDS_CHANNEL, EMBED_COLOR, PING_POLLING
from helpers import add_ping, check_msg_has_keyword, get_pings, save_pings


client = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())

pings = []

@client.event
async def on_ready():

    global pings

    pings = get_pings()


@client.event
async def on_message(message: discord.Message):

    if message.author.name != client.user.name and not message.content.startswith(COMMAND_PREFIX):
            
        msg_channel = message.channel.id
        pings_updated = False

        for ping in pings:

            keyword: str = ping["keyword"]
            timestamp: int = ping["timestamp"]
            role: discord.Role = get(message.guild.roles, id=ping["role"])
            channel: int = ping["channel"]

            if msg_channel == channel:

                now = int(time.time())

                if now - timestamp >= PING_POLLING and check_msg_has_keyword(message, keyword):

                    pings_updated = True

                    ping["timestamp"] = now
                    
                    await get(message.guild.channels, id=channel).send(role.mention)

        if pings_updated: save_pings(pings)

    await client.process_commands(message)


@client.command(name="addping")
async def add_new_ping(ctx: commands.Context, target_channel: discord.TextChannel, keyword: str, target_role: discord.Role):

    global pings

    if ctx.channel.id != COMMANDS_CHANNEL: return

    updated_pings = add_ping(target_channel, keyword, target_role)

    pings = updated_pings

    await ctx.send("new ping added successfuly")


@add_new_ping.error
async def add_new_ping_error(ctx, error):

    if isinstance(error, commands.RoleNotFound): await ctx.send("invalid role provided")
    if isinstance(error, commands.ChannelNotFound): await ctx.send("invalid channel provided")
    if isinstance(error, commands.MissingRequiredArgument): await ctx.send(error)


@client.command(name="listpings")
async def list_pings(ctx: commands.Context):

    if ctx.channel.id != COMMANDS_CHANNEL: return

    if not len(pings): return

    embed = Embed(
        color=EMBED_COLOR,
    )

    for i, ping in enumerate(pings):

        channel: discord.TextChannel = get(ctx.guild.channels, id=ping["channel"])
        role: discord.Role = get(ctx.guild.roles, id=ping["role"])
        keyword = ping["keyword"]

        embed.add_field(name=f"{i} " + "-"*50, value=f"{channel.mention} {role.mention} `{keyword}`", inline=False)

    await ctx.send(embed=embed)


@client.command(name="delping")
async def delete_ping(ctx: commands.Context, index: str):

    if ctx.channel.id != COMMANDS_CHANNEL: return

    if not index.isnumeric() or int(index) >= len(pings):

        await ctx.send("invalid index value provided")

        return
    
    del pings[int(index)]

    save_pings(pings)

    await ctx.send("ping deleted successfuly")


client.run(BOT_TOKEN)