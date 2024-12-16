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
  room_id = "65b8c6d08cc9a3e000c2a328"
  bot_token = "29e2a35451b882fc4641be91d7bb9b9d7fed9ff9cbf4c296a32422e451a3eca7"
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