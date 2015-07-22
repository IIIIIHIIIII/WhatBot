# -*- coding: utf-8 -*-
import MySQLdb
from block_io import BlockIo
import random
import string
import urllib
import json
import price
import requests
from config import config

def getApiKey(name):
    cur.execute("select aes_decrypt(coinapi,'%s') from whatdata where user = '%s'" %(key,name))
    return cur.fetchall()[0][0]
    
def coincheck(name):
    if not(userExists(name)):
        return "Not registered. Use !register"
    if not(apiExists(name)):
        return "Api key is not added."
    return ""

def coinAdd(text,name):
    if not(userExists(name)):
        return "Not registered. Use !register"
    
    api = text[1] 
    cur.execute("update whatdata set coinapi = aes_encrypt('%s','%s') where user = '%s'" %(api,key,name))
    db.commit()
    return "Api key added."

def cancelBidAsk(text,name,cancelType):
    stats = coincheck(name)
    if(stats):
        return stats
    api_key = getApiKey(name)
    oid = text[1]
    data = {"apiKey":api_key,"orderID":oid}
    header = {'content-type': 'application/json'}
    url = "https://api.coinsecureis.cool/v0/auth/%s" %(cancelType)
    post_data = requests.post(url,data = json.dumps(data),headers=header).json()
    if "error" in post_data.keys():
        return post_data["error"]
    if type(post_data["result"][0]) == dict:
        return "%s" %post_data["result"][0]["error"]
    return "%s (%s) cancelled." %(cancelType.replace("cancel",""),oid)
    
def placeBidAsk(text,name,createType):
    stats = coincheck(name)
    if(stats):
        return stats
    api_key = getApiKey(name)
    
    rate = int(float(text[1]) * 100)
    vol = int(float(text[2]) * 100000000)
    
    data = {"apiKey":api_key,"rate":rate,"vol":vol}
    header = {'content-type': 'application/json'}
    url = "https://api.coinsecureis.cool/v0/auth/%s" %(createType)
    
    post_data = requests.post(url,data = json.dumps(data),headers=header).json()
    if "error" in post_data.keys():
        return post_data["error"]
    if type(post_data["result"][0]) == dict:
        return "%s" %post_data["result"][0]["error"]
    return "%s created.\n ID : %s" %(createType.replace("create",""),post_data["result"][0])

def coinbal(name,baltype):
    stats = coincheck(name)
    if(stats):
        return stats
    api_key = getApiKey(name)
    data = {"apiKey":api_key}
    header = {'content-type': 'application/json'}
    url = "https://api.coinsecureis.cool/v0/auth/%s" %(baltype)
    post_data = requests.post(url,data = json.dumps(data),headers=header).json()
    amount = float(post_data["result"][0])
    if "fiat" in baltype:
        amount /= 100
        tag = "₹"
    else:
        amount /= 100000000
        tag = "B"
    if "error" in post_data.keys():
        return post_data["error"]
    return "Your coinsecure %s balance : %s%.2f" %(baltype.replace("balance",""),tag,amount)
    
def getCoinsecAddr(name):
    stats = coincheck(name)
    if(stats):
        return stats
    api_key = getApiKey(name)
    data = {"apiKey":api_key}
    header = {'content-type': 'application/json'}
    post_data = requests.post("https://api.coinsecureis.cool/v0/auth/getcoinaddresses",data = json.dumps(data),headers=header).json()
    if "error" in post_data.keys():
        return post_data["error"]
    return "Your coinsecure address : %s" %(post_data["result"][len(post_data["result"]) -1]["address"])

def rup(amount):
    inrusd = float(price.iu)

    value = amount * inrusd
    
    usddoge = float(price.ud)
    return int(usddoge * value)
    
def commands():
    return("!register - Register accont.\n !balance - Check your balance. \n !tip - Tip others. \n !tag - Check your tag."
    "\n !address - Check your address. \n !change - Change your tag. \n !market - check coin market. \n !convert - check n amount of coinA in coinB"
    "\n\n Coinsecure commands : \n!coinapi - Add coinsecure api. \n !cbid - Create bid. \n !dbid - Cancel bid. \n !cask - Create ask. \n !dask - Cancel ask"
    "\n!info - Check coinsecure market.\n !cbal - Check coin balance.\n !fbal - Check fiat balance.\n !addr - Get coinsecure address.")
    
def stats():
    cur.execute("select * from whatdata")
    data = cur.fetchall()
    tmp = "Registered users : %d" %(len(data))
    return tmp
    
def changeTag(text,name):
    newTag = text[1]
    
    if tagExists(newTag):
        return "%s is taken" %(newTag)
    else:
        cur.execute("update whatdata set tag = '%s' where user = '%s'" %(newTag,name))
        db.commit()
        return "Tag changed"


def getUserTag(name):
    if not(userExists(name)):
        return "Not registered. Use !register"
    else:
        cur.execute("select tag from whatdata where user = '%s'" %(name))
        return "Your tag : %s" %(cur.fetchall()[0][0])

def getUserAdd(name):
    if not(userExists(name)):
        return "Not registered. Use !register"
    else:
        cur.execute("select address from whatdata where user = '%s'" %(name))
        return "Your address : %s" %(cur.fetchall()[0][0])

def tip(text,name):
    ruppee = "off"
    if not(userExists(name)):
        return "Not registered. Use !register"
    else:
        try:
            if "rs" in text[2]:
                ruppee = "on"
                text[2] = text[2].replace("rs","")
            amount = int(text[2])
        except ValueError:
            return "Invalid amount : %r" %(text[2])
                
    if amount <= 0:
        return "Invalid amount : %r. should be > 1" %(text[2])
        
    receiver = text[1]
    print receiver
    if not(tagExists(receiver)):
        return "Tag doesn't exist"
    
    cur_bal = balance(name,"yes")
    if ruppee == "on":
        amount = rup(amount)
    if(amount > cur_bal):
        return "You tried to tip %d but you only have %d" %(amount,cur_bal)
    else:
        cur.execute("update whatdata set balance = balance + %d where tag = '%s'" %(amount,receiver))
        db.commit()
        cur.execute("update whatdata set balance = balance - %d where user = '%s'" %(amount,name))
        db.commit()
        sender = getUserTag(name).replace("Your tag :","")
        value = float(price.du)
        inr = float(price.ui)
        return "%s tipped Ð%d (₹%.2f) to %s" %(sender,amount,(amount*value) * inr ,receiver)

def getBal(name,x):
    cur.execute("select balance,address from whatdata where user = '%s'" %(name))
    fetch = cur.fetchall()
    tmp_bal = fetch[0][0]
    address = fetch[0][1]

    bal_data = blockIo.get_address_balance(addresses="%s" %(address))
    bal = int(float(bal_data["data"]["balances"][0]["available_balance"])) + tmp_bal
    
    if x == "diff":
        return bal - tmp_bal
    elif x == "all":
        return [tmp_bal,bal]
    if x == "pending":
        return  int(float(bal_data["data"]["balances"][0]["pending_received_balance"]))
    else:
        return bal

def getTxData(txid,way):
    if "in" in way:
        page = urllib.urlopen("https://chain.so/api/v2/get_tx_inputs/DOGE/%s" %(txid))
    else:
        page = urllib.urlopen("https://chain.so/api/v2/get_tx_outputs/DOGE/%s" %(txid))
    page_data = json.loads(page.read().decode('utf-8'))
    
    if "in" in way:
        return page_data["data"]["inputs"]
    return page_data["data"]["outputs"]

        

def withdraw(text,name):
    if not(userExists(name)):
        return "Not registered. Use !register"
    try:
        amount = int(text[2])
    except ValueError:
        return "Invalid amount : %r" %(text[2])
    if amount <= 0:
        return "Invalid amount : %r. should be > 1" %(text[2])
    address = text[1]
    local_bal,cur_bal = getBal(name,"all")
    
    if((amount + 1) > cur_bal):
        return "Withdraw failed: insufficient balance."
    else:
        try:
            data = blockIo.withdraw(amounts= "%d" %(amount), to_addresses="%s" %(address), pin="%s" %(pin))
        except:            
            return "Withdraw failed."
        if(data["status"] == "fail"):
            return "Withdraw failed."
            
        txid = data["data"]["txid"]
        inout = getTxData(txid,"in")
        
        for i in inout:
            print("%d %s"%(int(float(i["value"])),i["address"]))
            cur.execute("update whatdata set balance = balance + %d where address = '%s'" %(int(float(i["value"])),i["address"]))
            db.commit()
    
        inout = getTxData(txid,"out")      
        
        for i in inout:
            print("%d %s"%(int(float(i["value"])),i["address"]))
            cur.execute("update whatdata set balance = balance - %d where address = '%s'" %(int(float(i["value"])),i["address"]))
            db.commit()
                
        cur.execute("update whatdata set balance = balance - %d where user = '%s'" %((amount + 1),name))
        db.commit()
        
        return "Withdraw successfull.\n\n txid : %s" %(data["data"]["txid"])

def balance(name,val):
    if not(userExists(name)):
        return "Not registered. Use !register"
    else:
        print "here"
        pen = getBal(name,"pending")
        cur_bal = getBal(name,"")
        print "got value"
        if val == "yes":
            return cur_bal
        
        value = float(price.du)
        inr = float(price.ui)

        if not(pen):
            return "Balance : Ð%d (₹%.2f)" %(cur_bal,(cur_bal*value)*inr)
        else:
            return "Balance : Ð%d (₹%.2f) (Pending --> Ð%d)" %(cur_bal,(cur_bal*value) * inr,pen)
            
def getTag():
    tag = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    cur.execute("select * from whatdata where tag = '%s'" %(tag))

    if cur.fetchall():
        getTag()
    return tag

def tagExists(receiver):
    cur.execute("select * from whatdata where tag = '%s'" %(receiver))
    if cur.fetchall():
        return True
    return False
    
def userExists(name):
    cur.execute("select * from whatdata where user = '%s'" %(name))

    if cur.fetchall():
        return True
    return False
    
def apiExists(name):
    cur.execute("select coinapi from whatdata where user = '%s' and coinapi is not NULL" %(name))

    if cur.fetchall():
        return True
    return False    

def register(name):
    if  userExists(name):
        return "You are already registered."
    else:
        address = blockIo.get_new_address()["data"]["address"]
        tag = getTag()
        cur.execute("insert into whatdata(tag,user,address,balance) values('%s','%s','%s',0)" %(tag,name,address))
        db.commit()
        return "Your tipbot address : %s\nYour tag : %s\n\nUse !change to change your tag." %(address,tag)
    
def connectIO(pin,api):
    version = 2
    return BlockIo(api,pin,version)
    
db = MySQLdb.connect(host=config["mysql"]["host"],user=config["mysql"]["user"],passwd=config["mysql"]["passwd"],db=config["mysql"]["db"])
cur = db.cursor()
blockApi = config["blockIO"]["apiKey"] #Block.io api key
pin = config["blockIO"]["pin"] #Block.io pin
blockIo = connectIO(pin,blockApi)
key = config["mysql"]["aesKey"] #AES key