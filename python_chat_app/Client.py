#Mthoko


from socket import AF_INET, SOCK_DGRAM, socket
from datetime import datetime
import threading
import random
import os
import sys
from tkinter import*








class Client:
    text = None
    #######
    loginSock = socket(AF_INET,SOCK_DGRAM)
    clientSock = socket(AF_INET,SOCK_DGRAM)
    recvSock = socket(AF_INET,SOCK_DGRAM)
    groupSock = None
    retrvSock = None
    serverIP = None
    portN = None
    Name =""
    Recip =None

    def __init__(self,IP, win):
        ''' initiate login GUI '''
        self.serverIP =IP
        # widgets here
        self.win = win
        self.frameOne = Frame(self.win)
        self.frameOne.pack()
        

        self.label1 = Label(self.frameOne, text='FROM').pack()
        self.e1 = Entry(self.frameOne)
        self.e1.pack(fill=X)
        self.label2 = Label(self.frameOne, text='TO').pack(fill=X)
        self.e2 = Entry(self.frameOne)
        self.e2.pack(fill=X)

        self.label3 = Label(self.frameOne, text='OR').pack()
        self.grpBtn = Button(self.frameOne,text="GROUP", command= lambda: self.login(self.e1.get(),"GROUP"))
        self.grpBtn.pack()
        self.lgnBtn = Button(self.frameOne,text="LOGIN", command= lambda: self.login(self.e1.get(),self.e2.get()) )
        self.lgnBtn.pack()

    def genPort(self):
        '''Generate a random port to be used by client'''
        self.portN = random.randint(5004,6002)
        return self.portN

    def login(self, name, recip):
        '''Called when you click the login button or group button, sends details used by the client handler thread '''
        self.Name =name
        self.Recip=recip
        ip = self.genPort()
        print("Local Port: "+str(ip))
        loginstr = self.Name +"\n"+recip+"\n"+str(ip)

        try:
            byteStr = loginstr.encode()
            loginPort = 5002
            localHost ="127.0.0.1"
            self.loginSock.sendto(byteStr,(localHost,loginPort))
        except IOError as error:
            print(error)

    def startRun(self):
        ''' initiates the chat Gui and sockets '''
        self.chtwin =  Tk()
        self.chtwin.title("Client Chat")
        
        self.loginSock = socket(AF_INET,SOCK_DGRAM)
        self.clientSock = socket(AF_INET,SOCK_DGRAM)
        self.recvSock = socket(AF_INET,SOCK_DGRAM)
        
        self.recvSock.bind(("",self.portN))


        msgHandler = messageHandler(self.Name,self.recvSock,self.portN, self.chtwin)
        msgHandler.rcvRecip(self.Recip)
        msgHandler.setDaemon(True)
        msgHandler.start()
        
        
        self.chtwin.mainloop()

       

class messageHandler(threading.Thread):
    '''Handles receiving, sending and displaying chat messages, also initiates the chat GUI'''
    recvSock = socket(AF_INET,SOCK_DGRAM)
    recip =None
    username =""
    Ip =None
    portNo =None
    text = None

    def __init__(self, name, recvSock,portNo, win):
        threading.Thread.__init__(self)
        ##### shared variables
        self.recvSock = recvSock
        self.username = name
        self.portNo = portNo
        ##### GUI setup
        self.win = win
        self.menu = Menu(self.win)
        self.win.config(menu=self.menu)
        self.flmenu =Menu(self.menu)
        self.menu.add_cascade(label='Menu', menu=self.flmenu)
        self.flmenu.add_command(label='Get History', command=lambda:self.getHistory())
        self.frameTwo = Frame(self.win)
        self.frameTwo.pack()
        self.frameThree =Frame(self.win)
        self.frameThree.pack()

        self.text = Text(self.frameTwo, height=8, width=58)
        self.text.pack( fill=X)

        self.label4 = Label(self.frameThree, text='REPLY').pack(fill=X, side=LEFT)
        self.e3 = Entry(self.frameThree)
        self.e3.pack(fill=X,side=LEFT)
        self.sndBtn = Button(self.frameThree,text="SEND", command=lambda:self.sendRply())

        self.sndBtn.pack(fill=X, side=RIGHT)
       

    # getters
    def getUsername(self):
        return self.username
    def getRecipient(self):
        return self.recip
    def getIp(self):
        return self.Ip
    def getUsername(self):
        return self.portNo

    def rcvRecip(self, recip):
        '''
        Used to update the recipient from client class
        '''
        self.recip = recip

    def display(self,Msg):
        '''
        displays received messages on textfield 
        '''
        self.text.insert(END,Msg+"\n")

    def getHistory(self):
        '''
        Called through the menu to retrieve chat and messages received while offline
        '''
        flName =self.username+".txt"
        print("File name:"+ flName)
        try:
            with open(os.path.join(sys.path[0],flName), "r") as file:
                msglines = file.readlines()
                print(msglines)
                for Msg in msglines:
                    if len(Msg)>0:
                        print(Msg)
                        self.display(Msg)
            file.close()
        except FileNotFoundError:
            pass
        
    def sendRply(self ):
        '''
        Called when you click send, compiles and send message to server then clear input text in textfield
        '''
        resp = self.e3.get()+"\n"+ str(self.portNo)+"\n"+ (self.getRecipient())
        byteResp = resp.encode()
        self.recvSock.sendto(byteResp,("",5003))
        self.e3.delete(0,END)

    def run(self):
        '''
        overrides the run method with receive and display implementation
        '''
        try:
            while(True):
                bufferSize = 2048
                recvMsg, clientAddress = self.recvSock.recvfrom(bufferSize)
                Msg = recvMsg.decode()
                MsgL =Msg.split("\n")
                if len(MsgL) > 1:
                    print("One received by rcvSk:"+MsgL[1] +" "+ MsgL[0])
                    current = datetime.now()
                    dtStr = current.strftime("%d/%m/%Y %H:%M")
                    self.display( MsgL[1]+ " ["+ dtStr+"] "+MsgL[0])
                    
                else:
                    current = datetime.now()
                    dtStr = current.strftime("%d/%m/%Y %H:%M")
                    print("Two received by rcvSk:"+MsgL[0])
                    self.display("["+dtStr+"] "+MsgL[0])

         
        except OSError as error:
            print(error)



def main():
    '''
    initiate client class and login window
    '''
    lgnwin = Tk()
    lgnwin.title("Client Login")
    client = Client("127.0.0.1",lgnwin)
 
    lgnwin.mainloop()
    lgnwin.quit()
    client.startRun()

if __name__ == "__main__":
    main()