import requests, discord, re, time
import utils
from consts import consts
from discord.ext import tasks
from inspect import stack

# didnt test
@tasks.loop(minutes=5)
async def reqCheck():
    try:
        resp = requests.get(f"{consts.remoteDomain}", headers={"User-Agent" : "arabia-bot"}, timeout=10)
        if resp.status_code == 200 or resp.status_code == 403: return

        text = f"{resp.status_code} | {resp.reason}"
        await utils.LOGGER.log(stack()[0][3], text, "critical")

        vpsChannel = consts.bot.get_channel(consts.vpsChannel)
        embed = discord.Embed(title="ermmm", color=0x0084d1)
        embed.add_field(name="not optima", value=text)
        vpsChannel.send(embed=embed)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3], e, "error")