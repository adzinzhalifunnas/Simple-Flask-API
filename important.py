from datetime import datetime

class Important:
    def __init__(self, apikeyList):
        self.apikeyList = apikeyList

    def validateApiKey(self, apikeyList, apikey):
        if apikey in apikeyList:
            return True if apikeyList[apikey]['isAvailable'] and apikeyList[apikey]['isBanned'] == False else False

    def validatePremium(self, apikeyList, apikey):
        return True if apikeyList[apikey]['premium']['expires'] >= datetime.now().timestamp() else False

    def checkPremiumExpires(self, apikeyList, apikey):
        return datetime.fromtimestamp(apikeyList[apikey]['premium']['expires']).strftime('%Y-%m-%d %H:%M:%S')