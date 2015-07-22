import logging
import price
import time
import threading
from stack import YowsupEchoStack
from config import config

logging.basicConfig(level=logging.DEBUG)


t =  threading.Thread(target=price.getPrice)
t.start()
time.sleep(10)
credentials = (config["yowsup"]["phone"], config["yowsup"]["password"])
bot = YowsupEchoStack(credentials)
bot.start()
