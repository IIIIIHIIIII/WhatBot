import tipbot
import requests


answer = {}
    
def question(qfor):
    global answer
    try:
        answer[qfor]
        return "Wait for current trivia to end"
    except KeyError: 
        page = requests.get("http://jservice.io/api/random").json()
    
        question = page[0]["question"]
        answer[qfor] = page[0]["answer"] 
        print page[0]["answer"]
        return "Q : " + question
    
def ans(text,name,afrom):
    global answer
    
    try:
        answer[afrom]
    except KeyError:
        return False
    print answer[afrom]
    if(tipbot.userExists(name)):
        if " ".join(text).lower() == answer[afrom].lower():
            del(answer[afrom])
            return True
    return False