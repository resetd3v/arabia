import requests, discord, time, utils
import utils
from consts import consts
from discord.ext import commands, tasks
from inspect import stack

async def userlookup(interaction: discord.Interaction, userinput, ephemeralbool, priv, formattype):
    # from when it was slash cmds
    # try: priv = bool(priv)
    # except: priv = False
    if priv and not await utils.adminCheck(interaction):
        # i could log this and still send the embed but no
        await utils.LOGGER.discLog(stack()[0][3], interaction, "You can not use priv without admin", "error")
        return
    
    if formattype not in ("fields", "best"): formattype = "best"

    try:
        resp = requests.get(f"{consts.siteDomain}/api/users", headers=consts.headersLmao)
        if resp.status_code != 200:
            await utils.LOGGER.discLog(stack()[0][3], interaction, "Could retrieve user(s)", "error")
            return
        
        # TYPEHINTING JUST TO FUCKING SATISFY THIS ANNOYING ASS HIGHLIGHTING
        respJson:dict[dict] = resp.json()
        for user in respJson:
            # admin matches administrator even tho there is an acc called admin :/ so no "not in"
            if userinput not in user["username"]: continue
            embed = discord.Embed(title=f"User {user['username']}", color=0x0084d1)
            """
            match formattype:
                case "fields":
            """
            if formattype == "fields":
                for key, value in user.items():
                    # true false true | true false true    not (priv and utils.adminCheck(interaction)) and
                    if (not priv and (key == "token" or key == "totpSecret" or key == "oauth")) or key == "avatar": continue
                    inline = not (key == "domains") #or key == "embed")
                    embed.add_field(name=f"{key}", value=f"```{value}```", inline=inline)


                # rather use this than f"" \ ngl | nvm
            else:
                general = ("```ini\n"
                            f"[id] -> {user['id']}\n"
                            f"[username] -> {user['username']}\n"
                            f"[domains] -> {', '.join(user['domains'])}```"
                )
                
                role = (f"```ini\n"
                        f"[admin] -> {user['administrator']}\n"
                        f"[superAdmin] -> {user['superAdmin']}```"
                )
                
                if user["embed"]:
                    embedshit = (f"```ini\n"
                                f"[title] -> {user['embed']['title']}\n"
                                f"[description] -> {user['embed']['description']}\n"
                                f"[color] -> {user['embed']['color']}\n"
                                f"[override] -> {user['embed']['siteName']}```"
                    )
                else: embedshit = "```NULL```"

                misc = (f"```ini\n"
                        f"[rapelimit] -> {user['ratelimit']}\n"
                        f"[systemTheme] -> {user['systemTheme']}```"
                )
                
                embed.add_field(name=f"General", value=f"{general}", inline=False)
                embed.add_field(name=f"Role", value=f"{role}", inline=False)
                embed.add_field(name=f"Embed", value=f"{embedshit}", inline=False)
                embed.add_field(name=f"Misc", value=f"{misc}", inline=False)

                if priv:
                    priv = (f"```ini\n"
                            f"[token] -> {user['token']}\n"
                            f"[totpSecret] -> {user['totpSecret']}```"
                            #f"[oauth] -> {user["oauth"]}```"
                    )
                    embed.add_field(name=f"Priv", value=f"{priv}", inline=False)
        
            await interaction.response.send_message(embed=embed, ephemeral=ephemeralbool)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3], e, "error")
        await utils.LOGGER.discLog(stack()[0][3], interaction, "Could retrieve user(s)", "error")



# api doesnt support this rn (no way to get id from url) theres a few things missing :/
async def filelookup(interaction: discord.Interaction, url, priv, ephemeralbool):
    try: code = url.split("/")[-1]
    except: code = url

    try:
        resp = requests.get(f"{consts.siteDomain}/api/exif?id={code}", headers=consts.headersLmao)
        if resp != 200:
            await utils.LOGGER.log(stack()[0][3], resp.text, "error")
            await utils.LOGGER.discLog(stack()[0][3], interaction, f"Could not retrieve file from url/code | {url}", "error")
            return
        
        file = resp.json()
        embed = discord.Embed(title=f"File {file['name']}", color=0x0084d1)
        for key, value in enumerate(file):
            embed.add_field(name=key, value=f"```{value}```")

        await interaction.response.send_message(embed=embed, ephemeral=ephemeralbool)
    except Exception as e:
        await utils.LOGGER.log(stack()[0][3], e, "error")
