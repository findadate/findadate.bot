from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time


class WebServer():

  def __init__(self):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index() -> str:
      return "Funcionando"

  def run(self) -> None:
    self.app.run(host='0.0.0.0', port=8080)

  def keep_alive(self):
    t = Thread(target=self.run)
    t.start()


class RunBot():
  room_id = "64b557c588919e8f7b6fc5a6"
  bot_token = "37d64bfab92b753182072bd86c02a4f6269ec03a4acd3fd4f3acfc9dc39956b4"
  bot_file = "main"
  bot_class = "Bot"

  def __init__(self) -> None:
    self.definitions = [
        BotDefinition(
            getattr(import_module(self.bot_file), self.bot_class)(),
            self.room_id, self.bot_token)
    ]  # More BotDefinition classes can be added to the definitions list

  def run_loop(self) -> None:
    while True:
      try:
        arun(main(self.definitions))

      except Exception as e:
        print("Error: ", e)
        time.sleep(5)

if __name__ == "__main__":
  WebServer().keep_alive()

  RunBot().run_loop()
