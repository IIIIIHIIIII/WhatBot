import logging
import price
import time
import threading
from stack import YowsupEchoStack

logging.basicConfig(level=logging.DEBUG)


t =  threading.Thread(target=price.getPrice)
t.start()
time.sleep(10)
credentials = ("", "") # Whatsapp Phone,Password
bot = YowsupEchoStack(credentials)
bot.start()
