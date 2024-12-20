import discord, datetime, json, time, requests, json
import utils
from consts import consts
from plugins import *
from discord.ext import commands, tasks

# ik theres no status code checks or anything on any requests idc cope i have it on my other python "projects" (python code isnt projects)
# request lib soontm

#datetime.datetime.now(datetime.UTC)
bot = consts.bot
tree = bot.tree
prefix = consts.prefix

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    activityType = discord.Streaming(platform="Twitch", twitch_name="xqc", name="Spent 5mins trying to close confusing.wtf", game="confusing.wtf", url="https://twitch.tv/xqc")
    await consts.bot.change_presence(activity=activityType)
    if not consts.test:
        if not (statstask.statsTask.is_running() and cf.cfPrint.is_running()):
            cf.cfPrint.start()
            allah.reqCheck.start()
            statstask.statsTask.start()
        else:
            cf.cfPrint.restart()
            allah.reqCheck.restart()
            statstask.statsTask.restart()
    await bot.tree.sync()
    await utils.LOGGER.log(None, "".join([f"{command.name} " for command in bot.tree.get_commands()]), "debug")

#@bot.command()
# @bot.tree.command(name="help", description="What do u think")
# async def help(interaction: discord.Interaction):
#     try:
#         embed = discord.Embed(title="Help/Usage", color=0x0084d1)
#         # ebveyon comdmnds
#         embed.add_field(name="**@EVERYON**", value=f"```-> {prefix}stats [refresh]\nView the stats of the image host, these stats update every 30mins and refresh will force an update```", inline=False)
#         # admon coman
#         embed.add_field(name="**ADMON ONLI**", value=f"```-> {prefix}userlookup <user> [ephemeral] [priv]\nReturns all information the api provides about a user\n\n-> {prefix}giveinvite <user> [amount] [expiry]\nSends invite(s) to a users dms\n\n-> {prefix}geninvite [amount] [expiry] [ephemeral]\nSends invite(s) to the current channel, ephemeral is true by default\n\n-> {prefix}invitewave [amount] [expiry]\nSends invite(s) to all members with the user role in dms\n\n-> {prefix}viewinvites [ephemeral]\nReturns all active invites\n\n-> {prefix}removeinvites <code(s)>\nRemoves the invite(s) specified```", inline=False)
#         await interaction.response.send_message(embed=embed)
#     except Exception as e: print(e)

@bot.tree.command(name="ping", description="pinger!!11!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('pong1!1!!"')

@bot.tree.command(name="pong", description="pon!!11!")
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message('pin!14.')
                          
# genral cat
#@bot.command(aliases=["s", "stat"])
@bot.tree.command(name="stats", description="View the stats of the image host, these stats update every 30mins and refresh will force an update")
async def stats(interaction: discord.Interaction, refresh:bool=False, task:bool=False):
    await statstask.stats(interaction, refresh, task)

# admin
#@bot.command(aliases=["ul", "user", "userinfo"])
@bot.tree.command(name="cfmanual", description="..... no")
async def cfmanual(interaction: discord.Interaction):
    if await utils.adminCheck(interaction):
        cf.cfPrint.restart()

@bot.tree.command(name="userinfo", description="Returns all information the api provides about a user")
async def userlookup(interaction: discord.Interaction, user: str, ephemeral:bool=True, priv:bool=False, formattype:str="best"):
    await info.userlookup(interaction, user, ephemeral, priv, formattype)

@bot.tree.command(name="filelookup", description="Returns all information the api provides about a file")
async def filelookup(interaction: discord.Interaction, url: str, priv: bool=False, ephemeral: bool=True):
    await info.filelookup(interaction, url, priv, ephemeral)

#@bot.command(aliases=["gi", "giveinvites", "giveinvite"])
@bot.tree.command(name="giveinv", description="Sends invite(s) to a users dms")
async def giveinv(interaction: discord.Interaction, user: discord.User, amount:int=1, expiry:str="7d"):
    await invites.giveinvite(interaction, user, amount, expiry)

#@bot.command(aliases=["inv", "geninvites", "geninvite"])
@bot.tree.command(name="geninv", description="Sends invite(s) to the current channel, ephemeral is true by default")
async def geninv(interaction: discord.Interaction, amount: int=1, expiry: str="7d", ephemeral: bool=True):
    await invites.geninvite(interaction, amount, expiry, ephemeral)

#@bot.command(aliases=["vi", "viewinvite", "viewinvites"])
@bot.tree.command(name="viewinv", description="View active invites")
async def viewinv(interaction: discord.Interaction, ephemeral: bool=True):
    await invites.viewinvites(interaction, ephemeral)

#@bot.command(aliases=["iw", "invitewave"])
@bot.tree.command(name="invwave", description="Sends invite(s) to all members with the user role in dms")
async def invwave(interaction: discord.Interaction, amount: int=1, expiry: str="7d"):
    await invites.invitewave(interaction, amount, expiry)

#@bot.command(aliases=["ri", "removeinvite", "delinvite", "delinvites", "delinv", "delinvs"])
@bot.tree.command(name="delinv", description="Removes the invite(s) specified (only in slash cmds seperated by a comma)")
async def removeinvites(interaction: discord.Interaction, args: str):
    await invites.removeinvites(interaction, args)

try:
    #headersLmao = {"Cookie": f"user={uuid}:{base64.b64encode(hmac.new(secret.encode("UTF-8"), auth.encode(), hashlib.sha256).hexdigest().encode("ascii")).decode("ascii").replace("=", "")}"}

    bot.run(consts.token)
except Exception as e:
    print(f"[CRITICAL] Failed to get config file / bot token | {e}")