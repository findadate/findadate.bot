import os
import sys

# Step 1: Manual fix for 'pkg_resources' error
try:
    import pkg_resources
except ImportError:
    os.system('pip install setuptools')

from flask import Flask
from threading import Thread
import time
import asyncio
from importlib import import_module

# Step 2: Flexible Imports for Highrise
try:
    from highrise import BaseBot, BotDefinition
    from highrise.__main__ import main as highrise_main
except ImportError:
    # Agar purana path kaam kare toh
    from highrise.models import BaseBot, BotDefinition
    import highrise.__main__ as h_main
    highrise_main = h_main.main

class WebServer():
    def __init__(self):
        self.app = Flask(__name__)
        @self.app.route('/')
        def index(): return "Bot is Online!"
    def run(self):
        self.app.run(host='0.0.0.0', port=8080)
    def keep_alive(self):
        Thread(target=self.run, daemon=True).start()

class RunBot():
    room_id = "676c30efa4158157052f44f6"
    bot_token = "36e52099bb646d35c6e2f568c4728f52adcd7b4bf5664a41ee94c9905584c276"
    
    def __init__(self):
        try:
            # Ye 'main.py' ko load karega
            module = import_module("main")
            bot_instance = getattr(module, "Bot")()
            self.definitions = [BotDefinition(bot_instance, self.room_id, self.bot_token)]
        except Exception as e:
            print(f"Loading Error: {e}")
            self.definitions = []

    def run_loop(self):
        if not self.definitions: return
        while True:
            try:
                asyncio.run(highrise_main(self.definitions))
            except Exception as e:
                print(f"Bot Crashed: {e}. Restarting...")
                time.sleep(5)

if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_loop()
