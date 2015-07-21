# -*- coding: utf-8 -*-
import urllib
import json
import requests

def info():
    data = requests.get("https://api.coinsecure.in/v0/noauth/ticker").json()
    if "bid" in data["result"][3][0]["lasttrade"][0].keys():
        rate = (float(data["result"][3][0]["lasttrade"][0]["bid"][0][0]["rate"]) / 100)
    else:
        rate = (float(data["result"][3][0]["lasttrade"][0]["ask"][0][0]["rate"]) / 100)

    maxrate = (float(data["result"][1][0]["max24Hr"]) / 100)
    minrate = (float(data["result"][2][0]["min24Hr"]) / 100)
    
    return "Coinsecure Market.\n Rate : ₹%.2f\n MaxRate(1Day) : ₹%.2f\n MinRate(1Day) : ₹%.2f" %(rate,maxrate,minrate)

def market(text):
    coin = text[1]
    if coin.upper() == "BTC":
        coinB = "usd"
        tag = "$"
    else:
        coinB = "btc"
        tag = "B"

    page = urllib.urlopen("https://www.cryptonator.com/api/full/%s-%s" %(coin,coinB))
    page_data = json.loads(page.read().decode('utf-8'))
    if page_data["success"] == False:
        return "Coin not found"

    exchange = ["Cryptsy","Poloniex","Bittrex","Bitstamp","Cex.io","BTC38"]
    tmp = "%s Market" %(coin.upper())
    for i in range(1,len(page_data["ticker"]["markets"])):
        if page_data["ticker"]["markets"][i]["market"] in exchange:
            price = page_data["ticker"]["markets"][i]["price"]
            if tag == "$":
                tmp += "\n%s --> %s%.2f" %(page_data["ticker"]["markets"][i]["market"],tag,float(price))
            else:
                tmp += "\n%s --> %s%s" %(page_data["ticker"]["markets"][i]["market"],tag,price)

    return tmp
    
    
def convert(text):
    try:
        ogValue = float(text[1])
    except ValueError:
        return "Invalid amount %r" %(text[1])

    coinA = text[2].upper()
    coinB = text[3].upper()

    page = urllib.urlopen("https://www.cryptonator.com/api/ticker/%s-%s" %(coinA,coinB))
    page_data = json.loads(page.read().decode('utf-8'))


    if (page_data["error"]):
        return "%s" %(page_data["error"])
    else:
        value = float(page_data["ticker"]["price"])
        return "%f %s = %f %s" %(ogValue,coinA,(ogValue * value),coinB)