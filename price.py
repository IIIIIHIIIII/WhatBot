# -*- coding: utf-8 -*-
import untangle
import time
import requests

def getPrice():
    while True:
        global ui,iu,du,ud
        
        page_data = requests.get("http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json").json()

        for i in page_data['list']['resources']:
            if(i["resource"]["fields"]["name"] == "USD/INR"):
                ui = i["resource"]["fields"]["price"]
                break
            
        iu = str(1 / float(ui))

        data = requests.get("https://www.cryptonator.com/api/ticker/doge-usd").json()
        price = data["ticker"]["price"]
        du = price
        
        data = requests.get("https://www.cryptonator.com/api/ticker/usd-doge").json()
        price = data["ticker"]["price"]
        ud = price
        time.sleep(450)
        
ui = "0"
iu = "0"
du = ""
ud = ""
