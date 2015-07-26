# -*- coding: utf-8 -*-
import untangle
import time
import requests

def getPrice():
    while True:
        global ui,iu,du,ud
        
        #value = untangle.parse("http://www.webservicex.net/CurrencyConvertor.asmx/ConversionRate?FromCurrency=USD&ToCurrency=INR").double.cdata
        #ui = value
        
        #value = untangle.parse("http://www.webservicex.net/CurrencyConvertor.asmx/ConversionRate?FromCurrency=INR&ToCurrency=USD").double.cdata
        #iu = value

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
