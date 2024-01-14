#Mthoko
import os
from socket import AF_INET, SOCK_DGRAM, socket
import sys
import threading
from datetime import datetime

class Server:
    groupChatUsers = {}
    connected = {}
    serverSock = None
    loginSock = None
    sendSock = None

    def __init__(self):
        pass
        
    def getGroupChatUsers(self):
        return self.groupChatUsers

    def getConnected(self):
        return self.connected

    def startRun(self):
        '''initiate and bind sockets'''
        self.serverSock = socket(AF_INET, SOCK_DGRAM)
        self.serverSock.bind(("",5001))
        self.loginSock = socket(AF_INET, SOCK_DGRAM)
        self.loginSock.bind(("",5002))
        self.sendSock = socket(AF_INET, SOCK_DGRAM)
        self.sendSock.bind(("",5003))
        #Listen for login message and update local variables
        while(True):
            bufferSize = 2048
            login,lgnAdr = self.loginSock.recvfrom(bufferSize)
            data = login.decode().split("\n")
            print("Data from login "+str(data))
            userName = data[0]
            recipName = data[1]
            portNo = data[2]
            # attempts to read from text file and send recently sent messages
            flName = userName+".txt"
            try:
                with open(os.path.join(sys.path[0],flName), "r") as file:
                    while(file.read()):
                        print("File readlines --> "+str(file.readlines()))
                        byteMSg = file.read().encode()
                        if len(byteMSg)>0:
                            self.sendSock.sendto(byteMSg,("",int(portNo)))
                    file.close()
            except FileNotFoundError:
                pass
            # Invoke client Handler threads based on the recipient
            if recipName == "GROUP":
                grpUser = clientHandler(self.sendSock,userName, "GROUP", lgnAdr[0], portNo)
                gUsers = self.getGroupChatUsers()
                gUsers[userName] = grpUser.getPortNo()
                self.groupChatUsers = gUsers
                grpUser.recvGrp(self.groupChatUsers)
                if len(self.getGroupChatUsers()) > 1:
                    msg = userName + " Has Entered the Chat"
                    self.groupMsg(msg,"Server")
                    grpUser.daemon = True
                    grpUser.start()
            else:
                snglUser = clientHandler(self.sendSock,  userName,  data[1], lgnAdr[0], portNo)
                cons = self.getConnected()
                cons[userName] = snglUser.getPortNo()
                self.connected = cons
                snglUser.recvCon(self.connected)
                #Send notifications when new clients login
                if recipName in self.getConnected().keys():
                    notif = "You are Chatting with: "+userName
                    self.sendMsg(notif, "Server:",recipName)
                    snglUser.daemon = True
                    snglUser.start()
                    print("Msg sent")
                else:
                    notif = recipName+" is offline at the moment."
                    self.sendMsg(notif, "Server:", userName)
                    snglUser.daemon = True
                    snglUser.start()
                    print("Msg sent")                

    def sendMsg(self, Msg, sender,recip):
        '''concatinate message and message information then checks if recipient is connected the sends message'''
        try:
            msgInfo = Msg+"\n"+sender+"\n"+recip
            byteMsg = msgInfo.encode()
            if recip in self.getConnected().keys():
                print(self.getConnected().keys())
                print(self.getConnected().get(recip))
                #self.sendSock.bind(self.getConnected().get(recip))
                self.sendSock.sendto(byteMsg,("",int(self.getConnected().get(recip))))
        except IOError as error:
            print(error)

    def groupMsg(self, Msg, sender):
        '''concatinate message and message information then sends to every member of the group except sender'''
        msgInfo = Msg+"\n"+sender
        byteMsg = msgInfo.encode()
        for adr in self.getGroupChatUsers().values():
            if sender != adr:
                try:
                    self.sendSock.sendto(byteMsg,("",int(adr)))
                except IOError as error:
                    print(error)

class clientHandler(threading.Thread):
    '''Handles receiving messages from clients and sending to the appropriate recipient'''
    cltSock = socket(AF_INET,SOCK_DGRAM)
    userName = ""
    recip = ""
    ipAdr = None
    portNo = None
    groupChatUsers = {}
    connected = {}
    sendSock = None

    def __init__(self, cltSock, userName, recip, ipAdr, portNo):
        threading.Thread.__init__(self)
        self.cltSock = cltSock
        self.userName = userName
        self.recip = recip
        self.ipAdr = ipAdr
        self.portNo = portNo
        self.sendSock = socket(AF_INET, SOCK_DGRAM)

    # Getters    
    def getUsername(self):
        return self.userName

    def getConnected(self):
        return self.connected
    
    def getGroupChatUsers(self):
        return self.groupChatUsers
    
    def getRecipient(self):
        return self.recip
    
    def getIp(self):
        return self.ipAdr
    
    def getPortNo(self):
        return self.portNo

    def getAdr(self):
        return (self.ipAdr,self.portNo)

    #setters
    def recvCon(self,con):
        self.connected = con

    def recvGrp(self,con):
        self.groupChatUsers = con
    
    def getKeybyVal(self, val):
        '''Get key/username of the of the given value/port no from the connected dictionary'''
        for key, value in self.getConnected().items():
         if val == value:
             return key
        return "key doesn't exist"

    def writeChatLogs(self, Msg):
        '''Append chat logs if file already exist or create a new file and write chat logs'''
        userFlName = self.recip+".txt"
        try:
            with open(os.path.join(sys.path[0],userFlName), "a") as file:
                current = datetime.now()
                dtStr = current.strftime("%d/%m/%Y %H:%M")
                file.write(dtStr+" "+Msg)
                file.close()
        except FileNotFoundError:
            with open(os.path.join(sys.path[0],userFlName), "w") as file:
                current = datetime.now()
                dtStr = current.strftime("%d/%m/%Y %H:%M")
                file.write(dtStr+" "+Msg)
                file.close()
                    
        rcpFlName = self.userName+".txt"
        try:
            with open(os.path.join(sys.path[0],rcpFlName), "a") as file:
                current = datetime.now()
                dtStr = current.strftime("%d/%m/%Y %H:%M")
                file.write(dtStr+" "+Msg)
                file.close()
        except FileNotFoundError:
            rcpFlName = self.userName+".txt"
            with open(os.path.join(sys.path[0],rcpFlName), "w") as file:
                current = datetime.now()
                dtStr = current.strftime("%d/%m/%Y %H:%M")
                file.write(dtStr+" "+Msg)
                file.close()

    def run(self):
        '''Receives messages from clients and and sends it to recipient '''
        try:
            while(True):
                bufferSize = 2048
                recvMsg,cltAdr = self.cltSock.recvfrom(bufferSize)
                cltMsg = recvMsg.decode()
                cltMsgA = cltMsg.split("\n")
                print("clientMsg:\n"+cltMsg+"\nlen after split:"+str(len(cltMsgA)))
                #Msg = cltMsgA[0]
                sender = cltMsgA[1]
                recipi = cltMsgA[2]
                self.userName = self.getKeybyVal(sender)
                self.recip =recipi

                print("Sender: "+self.userName+"  Recipi :"+ recipi)                

                if recipi == "GROUP":
                    print(str(self.getRecipient)+":.To Group->:"+cltMsg)
                    self.groupMsg(cltMsg, sender)
                    self.writeChatLogs(cltMsg)
                else:
                    if(self.getKeybyVal(sender) == self.getRecipient() ):
                        #should use sending socket
                        print("From"+self.getUsername()+" Sending to:"+self.getRecipient())
                        self.sendMsg(cltMsgA[0],sender,self.getUsername())
                        self.writeChatLogs(cltMsg)
                    else:
                        print("From"+self.getUsername()+" Sending to:"+self.getRecipient())
                        self.sendMsg(cltMsgA[0],sender,self.getRecipient())
                        self.writeChatLogs(cltMsg)
                                        
        except IOError as error:
            print(error)

    def groupMsg(self, Msg, sender):
        '''encapulate send to group method to use it in client handler'''
        Server.groupMsg(self, Msg, sender)

    def sendMsg(self, Msg, sender,  recip):
        '''encapulate send message method to use it in client handler'''
        Server.sendMsg(self, Msg, sender, recip)

def main():
    '''Initiate server object and star server'''
    server = Server()
    print("Server running and Listening")
    server.startRun()

if __name__ == "__main__":
    main()