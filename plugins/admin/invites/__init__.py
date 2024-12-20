import requests, discord, datetime
import string, random
import utils
from consts import consts
from discord.ext import commands, tasks
from inspect import stack

"""
i should rlly recode this
typehinting is from when it wasnt slash cmds
api doesnt respond with a list if theres 1 invite soooooo
"""

async def invEmbed(interaction: discord.Interaction, invites, give:bool):
    # try: give = bool(give)
    # except: give = False
    single = len(invites) == 1 #type(invites) != list

    embed = discord.Embed(title=f"Invite{'s' if not single else ''}", url=f"{consts.remoteDomain}/auth/register?code={invites[0] if single else ''}", color=0x0084d1)
    if give: embed.description = f"An admin ({interaction.user.name}) has sent you {len(invites)} invite{'s' if not single else ''}\n{consts.remoteDomain}/auth/register?code={invites[0] if single else ''}\n"

    for invite in invites:
        embed.add_field(name="", value=f"```{invite}```")

    # inviteString = ""
    # for i, invite in enumerate(invites):
    #     inviteString += invite + ("\n" if not single and len(invites) - 1 != i else "")

    #embed.add_field(name="", value=f"```{inviteString}```")
    #embed.description += f"```{inviteString}```"

    embed.set_footer(text=f'Command ran by {interaction.user.name} at {datetime.datetime.utcnow()}')
    return embed


# two cmds combined into one thats y its messy
async def inv(interaction: discord.Interaction, get: bool, amount: int, expiry: str):
    if not await utils.adminCheck(interaction): return
    if not (not get and 0 < amount <= 20):
        await utils.LOGGER.discLog(stack()[0][3], interaction, "Invalid amount", "error")
        return None
    
    single = False
    invites = []
    method = requests.get if get else requests.post
    # jsonData if not get u pick
    jsonData = {"expiresAt": expiry, "count": amount} if not get else ""
    resp = method(f"{consts.siteDomain}/api/auth/invite", headers=consts.headersLmao, json=jsonData)
    # u choose two function calls or this who cares
    inviteData = resp.json()
    # try:
    #     list(inviteData)
    #     single = True
    # except Exception as e: pass
    single = type(inviteData) == dict

    # moment
    # amount > 1 or get  |  idk if get always responds with a list or ive just only tested when ive had multiple invs
    if single:
        try:
            invites = [inviteData["code"]]
        except: pass
        
    else: invites = [invite["code"] for invite in inviteData]
        

    if len(invites) == 0:
        await utils.LOGGER.log(stack()[0][3].upper(), f"{resp.status_code} | ({type(inviteData)}) {inviteData}", "error")
        await utils.LOGGER.discLog(stack()[0][3], interaction, "Could not gen/retrieve invite(s)", "error")
        return None
    return invites



async def invitewave(interaction: discord.Interaction, amount, expiry):
    if not await utils.adminCheck(interaction): return
    try: amount = int(amount)
    except: return
    await interaction.response.defer()

    # test invs
    #users = [interaction.guild.get_member(1216192858550304880), interaction.guild.get_member(709547527334002829)]
    # invites = []
    # for i in range(len(users) * amount):
    #     invites.append(''.join([random.choice(string.ascii_lowercase) for i in range(9)]))

    # put role in cfg soontm
    users: list[discord.User] = [user for user in interaction.guild.get_role(1213494436579774566).members] 
    invites = await inv(interaction, get=False, amount=len(users) * amount, expiry=expiry)

    if invites == None: return

    # idk what i was cookin but ti was somethin
    # 15 invites   2 invites per user 15 30  1st user (0 cuz indexing) 2 invs per, second inv = 1st inv good | 5th user (4) 4 + 1 5th inv | 2 (1) + 1
    # invite[0] invite[1] | amount=2 invites[0] + invites[1]
    # o(n^2) moment
    actualUser = 0
    inviteCount = 0
    for user in users:
        try:
            templist = []
            for _ in range(amount): templist.append(invites.pop(0))
            embed = await invEmbed(interaction, templist, give=True)
            await user.send(embed=embed)
            inviteCount += amount
            actualUser += 1
        except: pass

    await interaction.response.send_message(f"{inviteCount} ({amount}) Invites sent to {actualUser} users")



async def giveinvite(interaction: discord.Interaction, user: discord.User, amount, expiry):
    if not await utils.adminCheck(interaction): return

    try:
        invites = await inv(interaction, get=False, amount=amount, expiry=expiry)
        if invites == None: return

        embed = await invEmbed(interaction, invites, give=True)
        await user.send(embed=embed)
        await interaction.response.send_message(f"Invite sent to {user.name}")
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3].upper(), e, "error")
        await utils.LOGGER.discLog(stack()[0][3].upper(), interaction, "Could not send msg (user may have dms disabled)", "error")



async def geninvite(interaction: discord.Interaction, amount, expiry, ephemeralbool):
    if not await utils.adminCheck(interaction): return

    try: ephemeralbool = bool(ephemeralbool)
    except: ephemeralbool = False

    try:
        invites = await inv(interaction, get=False, amount=amount, expiry=expiry)
        if invites == None: return
        embed = await invEmbed(interaction, invites, give=False)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeralbool)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3].upper(), e, "error")
        await utils.LOGGER.discLog(stack()[0][3].upper(), interaction, "An unknown error occured", "error")



async def viewinvites(interaction: discord.Interaction, ephemeralbool):
    if not await utils.adminCheck(interaction): return
    try:
        invites = await inv(interaction, get=True, amount=0, expiry="0m")
        if invites == None:
            await utils.LOGGER.discLog(stack()[0][3], interaction, "Failed getting invites, its possible no invites exist", "error")
            return
        
        embed = await invEmbed(interaction, invites, give=False)
        await interaction.response.send_message(embed=embed, ephemeral=ephemeralbool)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3].upper(), e, "error")
        await utils.LOGGER.discLog(stack()[0][3].upper(), interaction, "An unknown error occured", "error")


# havent tested fully but it works
async def removeinvites(interaction: discord.Interaction, args:str):
    if not await utils.adminCheck(interaction): return
    counter = 0
    try:
        args = args.split(",")
        invitesdeleted = []
        thing = requests.get(f"{consts.siteDomain}/api/auth/invite", headers=consts.headersLmao).text
        for invite in args:
            if invite not in thing: continue
            resp = requests.delete(f"{consts.siteDomain}/api/auth/invite?code={invite}", headers=consts.headersLmao)
            if resp.status_code != 200: continue
            invitesdeleted.append(invite)
            counter +=1
    except: pass

    await interaction.response.send_message(f"Deleted {counter} invites | {invitesdeleted}") if counter != 0 else await utils.LOGGER.discLog(stack()[0][3], interaction, "Failed retrieving/deleting invites", "error")