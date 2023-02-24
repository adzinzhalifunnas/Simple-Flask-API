from flask import Flask, request, jsonify
from threading import Thread
from datetime import datetime
from important import Important
import asyncio, livejson

loop = asyncio.get_event_loop()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True
app.config['DEBUG'] = True

apikeyList = livejson.File('apikey.json', pretty=True, indent=4, sort_keys=True)

def messageOutput(code):
    return "Success" if code == 200 else "Invalid API Key" if code == 401 else "Error" if code == 500 else "Maintenance" if code == 503 else "Unknown"

def outputJson(data):
    return jsonify({'code': data['code'], 'message': messageOutput(data['code']), 'result': data['result']})

@app.route('/')
def index():
    return "Simple Flask API by Dzin"

@app.route('/api/validate', methods=['GET'])
def validate():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikeyList, apikey):
        return outputJson({'code': 200, 'result': True})
    else:
        return outputJson({'code': 401, 'result': False})

@app.route('/api/premium', methods=['GET'])
def premium():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikeyList, apikey):
        if Important(apikeyList).validatePremium(apikeyList, apikey):
            return outputJson({'code': 200, 'result': True})
        else:
            return outputJson({'code': 200, 'result': False})
    else:
        return outputJson({'code': 401, 'result': False})

@app.route('/api/premium/expire', methods=['GET'])
def premiumExpire():
    apikey = request.args.get('apikey')
    if Important(apikeyList).validateApiKey(apikeyList, apikey):
        if Important(apikeyList).validatePremium(apikeyList, apikey):
            return outputJson({'code': 200, 'result': {"isPremium": True, "message": "Your premium will expire on " + Important(apikeyList).checkPremiumExpires(apikeyList, apikey)}})
        else:
            return outputJson({'code': 200, 'result': {"isPremium": False, "message": "Your account is not premium or your premium has expired"}})
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