import requests, discord
import utils
from consts import consts
from discord.ext import commands, tasks
from inspect import stack

# not used anymore
global globalthing
globalthing = {"msg" : None}

@tasks.loop(hours=12)
async def statsTask():
    # if botStarted:
    #     botStarted = False
    #     statsTask.cancel()
    msg = None
    channel = consts.bot.get_channel(consts.statsChannel)
    # Y TF DOES THIS HNOT WORK CHECK IN DEBUG EVERYTHINGS FINE
    #msg = [msgObj async for msgObj in channel.history(limit=10) if msgObj.author.id == consts.bot.user.id][0]
    async for msgObj in channel.history(limit=10):
        if msgObj.author.id == consts.bot.user.id:
            msg = msgObj
            break
    
    try:
        #msg = globalthing["msg"]
        if not msg:
            msg = await channel.send(embed=await stats(None, refresh=True, task=True))
            return
        
        msg = await msg.edit(embed=await stats(None, refresh=True, task=True))
    except: msg = None

# statsTask.before_loop
# async def statsWait():


async def stats(interaction: discord.Interaction, refresh, task):
    try:
        # try: refresh = bool(refresh)
        # except: refresh = False

        if refresh:
            refreshResp = requests.post(f"{consts.siteDomain}/api/stats", headers=consts.headersLmao)
            await utils.LOGGER.log(stack()[0][3], refreshResp.text, "debug")

        resp = requests.get(f"{consts.siteDomain}/api/stats?amount=1", headers=consts.headersLmao)
        if resp.status_code != 200: return

        respData = resp.json()[0]
        embed = discord.Embed(title="Stats", color=0x0084d1)
        embed.add_field(name="Timestamp", value=f'```{respData["createdAt"]}```')
        embed.add_field(name="Size", value=f'```{respData["data"]["size"]}```')
        embed.add_field(name="File Count", value=f'```{respData["data"]["count"] }```')
        embed.add_field(name="User Count", value=f'```{respData["data"]["count_users"]}```')
        if task: return embed
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3], e, "error")
        if task: return
        await utils.LOGGER.discLog(stack()[0][3], interaction, "Unknown exception", "error")
