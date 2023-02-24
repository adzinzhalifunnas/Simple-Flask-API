from flask import Flask, request, jsonify
from threading import Thread
from datetime import datetime
from important import Important
from bs4 import BeautifulSoup
import asyncio, livejson, requests, traceback

loop = asyncio.get_event_loop()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True
app.config['DEBUG'] = True

apikeyList = livejson.File('apikey.json', pretty=True, indent=4, sort_keys=True)

def messageOutput(code):
    return "Success" if code == 200 else "Invalid API Key" if code == 401 else "Error" if code == 500 else "Maintenance" if code == 503 else "Unknown"

def outputJson(data):
    return jsonify({'code': data['code'], 'message': messageOutput(data['code']), 'result': data['result']})

def logError(error, write=True):
        result = traceback.format_exc()
        if write:
            with open('logError.txt', 'a') as f:
                f.write("\n%s"%result)

@app.route('/')
def index():
    return "Simple Flask API by Dzin"

@app.route('/api/validate', methods=['GET'])
def validate():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikey):
        return outputJson({'code': 200, 'result': True})
    else:
        return outputJson({'code': 401, 'result': False})

@app.route('/api/premium', methods=['GET'])
def premium():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikey):
        if Important(apikeyList).validatePremium(apikey):
            return outputJson({'code': 200, 'result': True})
        else:
            return outputJson({'code': 200, 'result': False})
    else:
        return outputJson({'code': 401, 'result': False})

@app.route('/api/premium/expire', methods=['GET'])
def premiumExpire():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikey):
        if Important(apikeyList).validatePremium(apikey):
            return outputJson({'code': 200, 'result': {"isPremium": True, "message": "Your premium will expire on " + Important(apikeyList).checkPremiumExpires(apikey)}})
        else:
            return outputJson({'code': 200, 'result': {"isPremium": False, "message": "Your account is not premium or your premium has expired"}})
    else:
        return outputJson({'code': 401, 'result': False})

@app.route('/api/kbbi', methods=['GET'])
def kbbi():
    apikey = request.args.get('apikey')
    type = request.args.get('type')
    if Important(apikeyList).validateApiKey(apikey):
        if type == "page":
            page = request.args.get('page')
            if page == None or not page.isdigit():
                return outputJson({'code': 500, 'result': {"message": "Invalid parameter. Need: page (int)"}})
            else:
                try:
                    with requests.session() as web:
                        web.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                        web = web.get("https://www.kbbi.co.id/daftar-kata?page={}".format(str(page)))
                        data = BeautifulSoup(web.content, "lxml")
                        result = []
                        for i in data.findAll("div", {"class":"row"}):
                            for j in i.findAll("div", {"class":"col-md-2 col-sm-3 col-xs-4"}):
                                for k in j.findAll("ul"):
                                    for l in k.findAll("li"):
                                        words = l.a.text
                                        urls = l.a['href']
                                        result.append({"word": words, "url": urls})
                        return outputJson({'code': 200, 'result': result})
                except Exception as e:
                    logError(e)
                    return outputJson({'code': 500, 'result': {"message": "Error from server"}})
        elif type == "word":
            if Important(apikeyList).validatePremium(apikey):
                word = request.args.get('word')
                if word == None:
                    return outputJson({'code': 500, 'result': {"message": "Invalid parameter. Need: word (string)"}})
                else:
                    try:
                        with requests.session() as web:
                            web.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
                            web = web.get("https://www.kbbi.co.id/arti-kata/{}".format(str(word)))
                            data = BeautifulSoup(web.content, "lxml")
                            result = []
                            for i in data.findAll("div", {"class":"row"}):
                                for j in i.findAll("div", {"class":"col-sm-8"}):
                                    for k in j.findAll("p", {"class":"arti"}):
                                        definitions = k.text
                                        result.append({"word": word, "description": "Arti kata, ejaan, dan contoh penggunaan kata %s menurut Kamus Besar Bahasa Indonesia (KBBI)."%(word), "definition": definitions})
                            if result == []:
                                return outputJson({'code': 200, 'result': {"message": "Word '%s' not found"%(word)}})
                            else:
                                return outputJson({'code': 200, 'result': result})
                    except Exception as e:
                        logError(e)
                        return outputJson({'code': 500, 'result': {"message": "Error from server"}})
            else:
                return outputJson({'code': 200, 'result': {"message": "This feature is only available for premium users"}})
        else:
            return outputJson({'code': 500, 'result': {"message": "Invalid type"}})
    else:
        return outputJson({'code': 401, 'result': False})

def running():
    app.run()

def run():
    threads = Thread(target=loop.run_until_complete(running()))
    threads.daemon = True
    threads.start()
    
if __name__ == '__main__':
    run()