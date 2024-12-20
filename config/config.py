import json
#import utils
from inspect import stack

class Config():
    def __init__(self):
        try:
            # time this
            # y tf cant u use read here cuz of the class? idk bruh python moment
            # fucking python 3.8  |  __file__.replace(__file__.split('\\')[-1], "")
            with open(f"{__file__.replace('config.py', '')}config.json", "r") as self.configFile:
                self.config: dict = json.load(self.configFile)
                self.verify()
        except Exception as e:
            #utils.LOGGER.log(stack()[0][3], e, "critical")
            print(f"[CRITICAL] ({stack()[0][3]}) {e}")
            exit()

    def save(self):
        try:
            if not self.verify(): raise BrokenPipeError
            with open(self.configFile.name, "w") as configFileWrite:
                json.dump(self.config, configFileWrite, ensure_ascii=False)

        except BrokenPipeError:
            #utils.LOGGER.log(stack()[0][3], f"Error saving config verify failed | {e} | {self.config}", "critical")
            print(f"[CRITICAL] ({stack()[0][3]}) Error saving config verify failed | {e} | {self.config}")
            exit()
        except Exception as e:
            #utils.LOGGER.log(stack()[0][3], f"Error saving config | {e} | {self.config}", "critical")
            print(f"[CRITICAL] ({stack()[0][3]}) Error saving config | {e} | {self.config}")
            exit()

    def verify(self):
        try:
            if self.config == None or "valid" not in self.config.keys():
                raise BufferError
            return True
        except Exception as e:
            #utils.LOGGER.log(stack()[0][3], f"Error verifying config | {e if type(e) != BufferError else 'INVALID'} | {self.config}", "critical")
            print(f"[CRITICAL] ({stack()[0][3]}) Error verifying config | {e if type(e) != BufferError else 'INVALID'} | {self.config}")
            exit()
            # \/ wont be hit
            return False
    
configObj = Config()
config = configObj.config