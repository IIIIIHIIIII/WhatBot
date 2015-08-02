# -*- coding: utf-8 -*-
import requests
import json
from requests.auth import HTTPBasicAuth
import tipbot
import math



def getOperator(text):
    
    headers = {
    'Content-Type': 'application/json'
    }
    
    data = requests.get("https://api.bitrefill.com/v1/lookup_number?number=%s"%(text),auth=HTTPBasicAuth(Key,Secret),headers=headers).json()    
    if "error" in data:
        return "Error :" + data["error"]["message"]
    if(data["operator"] == False):
        return "Error :" + data["message"]
    return data["operator"]["slug"]
    
def placeOrder(text,name):
    if not(tipbot.userExists(name)):
        return "Not registered. Use !register"
    op = getOperator(text[1])
    
    if("Error" in op):
        return op
    
    values = {
    "operatorSlug": op,
    "valuePackage" : str(int(float(text[2]))),
    "number" : text[1],
    "email" : ""
    }

    headers = {
    'Content-Type': 'application/json'
   }

    data = requests.post("https://api.bitrefill.com/v1/order/",auth=HTTPBasicAuth(Key,Secret),data=json.dumps(values),headers=headers).json()
    if "error" in data:
        return data["error"]["message"]
    orderId = data["orderId"]
    btcprice = data["btcPrice"]
    address = data["payment"]["address"]

    shapedata = {"amount":float(btcprice),"withdrawal":address, "pair":"DOGE_BTC"}    
    
    shape = requests.post("https://shapeshift.io/sendamount/",data = json.dumps(shapedata),headers=headers).json()
    if "error" in shape:
        return shape["error"]
    process = tipbot.withdraw(["",shape["success"]["deposit"],str(math.ceil(float(shape["success"]["depositAmount"])))],name)
    
    if("successfull." not in process):
        cancelShapeData = {"address":shape["success"]["deposit"]}
        requests.post("https://shapeshift.io/cancelpending/",data = json.dumps(cancelShapeData),headers=headers)
        return process
    return "Success. \n Id : %s" %(orderId)
    
Key = ""
Secret = ""