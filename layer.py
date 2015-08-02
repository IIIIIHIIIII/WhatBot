from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
import tipbot
import crypto
import threading 
import bitrefill
import wiki
import trivia
import time

class EchoLayer(YowInterfaceLayer):

    disable = []
    def cleanList(self,text):
        while "" in text:
            text.remove("")
        return text
    
    def displayText(self,gotMessage,messageProtocolEntity):
        reply = bitrefill.placeOrder(gotMessage,messageProtocolEntity.getFrom())
        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
        self.disable.remove(messageProtocolEntity.getFrom())
        self.toLower(messageEntity)
    
    def Timer(self,qfor,messageProtocolEntity):
        time.sleep(25)
        try:
            trivia.answer[qfor]
            del(trivia.answer[qfor])
            reply = "Trivia timeout."
            messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
            self.toLower(messageEntity)
        except KeyError:
            pass
        
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if True:
            if messageProtocolEntity.getType() == 'text':
                receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
                self.toLower(receipt)
                gotMessage = self.cleanList(messageProtocolEntity.getBody().split(" "))

                if (messageProtocolEntity.getParticipant() and messageProtocolEntity.getParticipant() not in self.disable):
                    if(gotMessage[0] == "!register" and len(gotMessage) == 1):
                        reply = tipbot.register(messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!balance" and len(gotMessage) == 1):
                        reply = tipbot.balance(messageProtocolEntity.getParticipant(),"")
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!tip" and len(gotMessage) == 3):
                        reply = tipbot.tip(gotMessage,messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!tag" and len(gotMessage) == 1):
                        reply = tipbot.getUserTag(messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!withdraw" and len(gotMessage) == 3):
                        reply = tipbot.withdraw(gotMessage,messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!address" and len(gotMessage) == 1):
                        reply = tipbot.getUserAdd(messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!change" and len(gotMessage) == 2):
                        reply = tipbot.changeTag(gotMessage,messageProtocolEntity.getParticipant())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!help" and len(gotMessage) == 1):
                        reply = tipbot.commands()
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getParticipant())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!market" and len(gotMessage) == 2):
                        reply = crypto.market(gotMessage)
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!convert" and len(gotMessage) == 4):
                        reply = crypto.convert(gotMessage)
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!info" and len(gotMessage) == 1):
                        reply = crypto.info()
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!trivia" and len(gotMessage) == 1):
                        reply = trivia.question(messageProtocolEntity.getFrom())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                        threading.Thread(target=self.Timer,args=(messageProtocolEntity.getFrom(),messageProtocolEntity)).start()
                    elif(gotMessage[0] == "!ans" and len(gotMessage) >= 2):
                        result = trivia.ans(gotMessage[1:],messageProtocolEntity.getParticipant(),messageProtocolEntity.getFrom())
                        if result:
                            reply = "Correct!"
                            messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                            self.toLower(messageEntity)
                            reply = tipbot.tip(["",tipbot.getUserTag(messageProtocolEntity.getParticipant()).replace("Your tag : ",""),"10"],"919892633961@s.whatsapp.net")
                            messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                            self.toLower(messageEntity)
                    elif(gotMessage[0] == "!wiki" and len(gotMessage) >= 2):
                        for i in range(2,len(gotMessage)):
                            gotMessage[i] = gotMessage[i].capitalize()
                        reply = wiki.getWiki("%20".join(gotMessage[1:]))
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!cbid" or gotMessage[0] == "!cask" and len(gotMessage) == 3):
                        if gotMessage[0] == "!cbid":
                            createType = "createbid"
                        else:
                            createType = "createask"
                        reply = tipbot.placeBidAsk(gotMessage,messageProtocolEntity.getParticipant(),createType)
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!dbid" or gotMessage[0] == "!dask" and len(gotMessage) == 2):
                        if gotMessage[0] == "!dbid":
                            cancelType = "cancelbid"
                        else:
                            cancelType = "cancelask"
                        reply = tipbot.cancelBidAsk(gotMessage,messageProtocolEntity.getParticipant(),cancelType)
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!fbal" or gotMessage[0] == "!cbal" and len(gotMessage) == 1):
                        if gotMessage[0] == "!fbal":
                            baltype = "fiatbalance"
                        else:
                            baltype = "coinbalance"
                        reply = tipbot.coinbal(messageProtocolEntity.getParticipant(),baltype)
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                elif(messageProtocolEntity.getFrom() not in self.disable):
                    if(gotMessage[0] == "!coinapi" and len(gotMessage) == 2):
                        reply = tipbot.coinAdd(gotMessage,messageProtocolEntity.getFrom())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!addr" and len(gotMessage) == 1):
                        reply = tipbot.getCoinsecAddr(messageProtocolEntity.getFrom())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!refill" and len(gotMessage) == 3):
                        self.disable.append(messageProtocolEntity.getFrom())
                        threading.Thread(target=self.displayText, args =(gotMessage,messageProtocolEntity)).start()
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
            
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
        
