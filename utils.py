import requests, discord, debug
from consts import consts
from discord.ext import commands
from urllib.parse import unquote
from inspect import stack

# button momento (player list) from stackoverflow cuz fuck you who cares
class Buttons(discord.ui.View):
    def __init__(self, server, *, timeout=180):
        super().__init__(timeout=timeout)
        self.server = server
    @discord.ui.button(label="Player List", style=discord.ButtonStyle.gray)
    async def playerListButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        #players = str([unquote(player) for player in self.server["playerData"]])
        embed = discord.Embed(title="Player List", color=0x0084d1)
        players = ""
        for player in self.server["playerData"]:
            players += f'{unquote(player)}\n'
        embed.add_field(name="", value=f"```{players}```", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def adminCheck(interaction: discord.Interaction):
    # confusing srv
    dotRole = interaction.guild.get_role(1213494436672180225)

    try:
        if (dotRole in interaction.user.roles): return True
    except: pass
    await interaction.response.send_message(f"no.")
    return False

class Logger():
    def __init__(self, discEphemeral):
        self.discEphemeral = discEphemeral

    async def log(self, function:str, msg, type:str, level=1, **kwargs):
        if type.upper() == "DEBUG" and level > consts.debug["level"]: return
        
        function = f" ({function.lower()})" if function else ""
        print(f"[{type.upper()}]{function} {msg}", **kwargs)

        # :tf:
        if type.upper() == "CRITICAL": exit()

    async def discLog(self, function:str, interaction:discord.Interaction, msg, type:str, level=1, **kwargs):
        if type.upper() == "DEBUG" and level > consts.debug["level"]: return
        function = f" ({function.lower()})" if function else ""
        # i overuse ternary idc
        await interaction.response.send_message(content=f"[{type.upper()}]{function} {msg}", ephemeral=True if type in ("error", "warn", "debug") and self.discEphemeral else False, **kwargs)
    
    #discLog: callable[discord.Interaction, str, str, None] = lambda interaction, msg, type, *args: interaction.response.send_message(msg, ephemeral=(type in ("error", "debug"), args))


LOGGER:Logger = Logger(True)