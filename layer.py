from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
import tipbot
import crypto

class EchoLayer(YowInterfaceLayer):

    def cleanList(self,text):
        while "" in text:
            text.remove("")
        return text
        
    
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        global disable
        if True:
            if messageProtocolEntity.getType() == 'text':
                print messageProtocolEntity
                receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
                self.toLower(receipt)
                gotMessage = self.cleanList(messageProtocolEntity.getBody().split(" "))

                if (messageProtocolEntity.getParticipant()):
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
                else:
                    if(gotMessage[0] == "!coinapi" and len(gotMessage) == 2):
                        reply = tipbot.coinAdd(gotMessage,messageProtocolEntity.getFrom())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
                    elif(gotMessage[0] == "!addr" and len(gotMessage) == 1):
                        reply = tipbot.getCoinsecAddr(messageProtocolEntity.getFrom())
                        messageEntity = TextMessageProtocolEntity(reply,to = messageProtocolEntity.getFrom())
                        self.toLower(messageEntity)
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))
            
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)
        
