from flask import Flask
from threading import Thread
import time
import asyncio
import highrise
# Hum dono jagah try karenge taaki error na aaye
try:
    from highrise import BaseBot, BotDefinition
except ImportError:
    from highrise.models import BaseBot, BotDefinition

from highrise.__main__ import main as highrise_main
from importlib import import_module

# 1. WebServer Setup
class WebServer():
    def __init__(self):
        self.app = Flask(__name__)
        @self.app.route('/')
        def index() -> str:
            return "Bot is Running!"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8080)

    def keep_alive(self):
        t = Thread(target=self.run, daemon=True)
        t.start()

# 2. Bot Runner Setup
class RunBot():
    room_id = "676c30efa4158157052f44f6"
    bot_token = "36e52099bb646d35c6e2f568c4728f52adcd7b4bf5664a41ee94c9905584c276"
    bot_file = "main" 
    bot_class = "Bot"

    def __init__(self) -> None:
        try:
            module = import_module(self.bot_file)
            bot_instance = getattr(module, self.bot_class)()
            self.definitions = [
                BotDefinition(bot_instance, self.room_id, self.bot_token)
            ]
        except Exception as e:
            print(f"Error loading bot: {e}")
            self.definitions = []

    def run_loop(self) -> None:
        if not self.definitions:
            print("No bot definitions found.")
            return

        while True:
            try:
                # Direct asyncio loop
                asyncio.run(highrise_main(self.definitions))
            except Exception as e:
                print(f"Bot Crashed: {e}. Restarting in 5s...")
                time.sleep(5)

if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_loop()
