from datetime import datetime

class Important:
    def __init__(self, apikeyList):
        self.apikeyList = apikeyList

    def validateApiKey(self, apikey):
        if apikey in self.apikeyList:
            return True if self.apikeyList[apikey]['isAvailable'] and self.apikeyList[apikey]['isBanned'] == False else False

    def validatePremium(self, apikey):
        return True if self.apikeyList[apikey]['premium']['expires'] >= datetime.now().timestamp() else False

    def checkPremiumExpires(self, apikey):
        return datetime.fromtimestamp(self.apikeyList[apikey]['premium']['expires']).strftime('%Y-%m-%d %H:%M:%S')