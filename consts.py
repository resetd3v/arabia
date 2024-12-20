import json, discord
from discord.ext import commands
from discord import app_commands
from inspect import stack
#import utils as utils
from config.config import config
from debug import debug

class Consts():
    def __init__(self):
        try:
            self.config = config
            self.debug = debug().debug
            self.test = False
            self.token = self.config["discord"]["token"] # if not self.test else self.config["discord"]["token2"]
            self.prefix = "/"
            self.bot = commands.Bot(command_prefix=self.prefix, intents=discord.Intents.all(), help_command=None)
            self.guildID = self.config["discord"]["guild"]
            self.siteDomain = self.config["site"]["domain"]
            self.remoteDomain = self.config["site"]["remoteDomain"]
            self.secret = self.config["site"]["secret"]
            self.siteAuth = self.config["site"]["auth"]
            #self.uuid = self.config["site"]["uuid"]
            self.statsChannel = self.config["site"]["statsChannel"]
            self.vpsChannel = self.config["site"]["vpsChannel"]
            self.cfAuth = self.config["cf"]["apiKey"]
            self.cfZone = self.config["cf"]["zoneID"]
            self.headers = {"User-Agent" : "arabia-bot"}
            self.headersLmao = {"Authorization" : f"{self.siteAuth}", "User-Agent" : "arabia-bot"}
            self.cfheadersLmao = {"Authorization" : f"Bearer {self.cfAuth}", "User-Agent" : "arabia-bot"}
        except Exception as e:
            #utils.LOGGER.log(stack()[0][3], e, "critical")
            print(f"[CRITICAL] ({stack()[0][3]}) {e}")
            exit()

consts = Consts()