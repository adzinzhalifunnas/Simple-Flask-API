from flask import Flask
from threading import Thread
import asyncio

loop = asyncio.get_event_loop()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = True
app.config['DEBUG'] = True

@app.route('/')
def index():
    return "Simple Flask API by Dzin"

def running():
    app.run()

def run():
    threads = Thread(target=loop.run_until_complete(running()))
    threads.daemon = True
    threads.start()
    
if __name__ == '__main__':
    run()