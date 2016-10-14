import socket
import sys
import threading
import os
import time
import random
import Queue

class Packet(object):
    def __init__(self, serializedString):
        self.seqNumber, self.character = serializedString.split(':', 1)
        self.seqNumber = int(self.seqNumber)
        self.serialized = serializedString
        self.ackRecvd   = False
        self.sent       = time.time()%60
    
    def getSerialized(self):
        return self.serialized
    
    def getAckRcvd(self):
        return self.ackRecvd
    
    def setAckRcvd(self, rcv):
        self.ackRecvd = rcv
    
    def send(self):
        self.sent = time.time()%60

    def getSent(self):
        return self.sent
    
    def getCharacter(self):
        return self.character

#Node representation. Superclass containing server, middle, and client.     
class Node(object):
    def __init__(self, mode, port, name):
        self.mode  = mode #1 for debug, 0 for standard
        self.port  = port
        #TCP/IP socket for use:
        self.sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name  = name

    def connect(self):
        connectAddress = ('localhost',self.port)
        print (self.name,'Client connected to', connectAddress)
        self.sock.connect(connectAddress)

    def bind(self):
        bindAddress = ('localhost',self.port)
        self.sock.bind(bindAddress)
        print (self.name,'Server binded to', bindAddress)

    def closeSocket(self):
        self.sock.close()
    
    def listen(self):
        self.sock.listen(1)
    
    def debug(self, message):
        if self.mode is 1: print self.name + message 

                                            
class Client(Node):
    def __init__(self, mode, port, timeout, windowSize, name):
        super(Client,self).__init__(mode, port, name)
        self.packetList = []
        self.lower = 0 #lower and upper to handle sliding window
        self.upper = windowSize - 1
        self.windowSize = windowSize
        self.timeout    = timeout
        print 'Client node started'

    def readFromFile(self, filename):
        self.debug('Reading and parsing from file into list')
        with open(filename) as f:
            seqNumber = 0
            while True:
                readChar = f.read(1)
                if not readChar:
                    break
                sequenceNumber = str(seqNumber) #normalize all possible numbers
                if len(str(seqNumber))   is 1: sequenceNumber = "0000"+str(seqNumber)
                elif len(str(seqNumber)) is 2: sequenceNumber = "000" +str(seqNumber)
                elif len(str(seqNumber)) is 3: sequenceNumber = "00"  +str(seqNumber)
                elif len(str(seqNumber)) is 4: sequenceNumber = "0"   +str(seqNumber)
                serialized = sequenceNumber+":"+str(readChar)
                seqNumber += 1 

                self.packetList.append(Packet(serialized))
            if len(self.packetList) < 10001: self.packetList.append(Packet('10001:z'))
        self.debug('Reading done. Total '+str(len(self.packetList))+' nodes to send.')

    def sendPacket(self, index):
        packet = self.packetList[index].getSerialized()
        self.debug('Sending packet: ' + packet + ' to server') 
        self.packetList[index].send()
        self.sock.send(packet)
    
    def checkTime(self):
        i = self.lower
        while i <= self.upper:
            # print (self.packetList[i].getSent()+self.timeout, 'timeout')  
            # print (time.time()%60, 'nein')
            if self.packetList[i].getAckRcvd() is False and self.packetList[i].getSent()+self.timeout > time.time()%60:
                self.sendPacket(i)

    def sendWindow(self):
        i = self.lower
        while i <= self.upper:
            self.sendPacket(i)
            i += 1

    def slideWindowBy(self, number):
        if self.upper+1 < len(self.packetList):
            self.debug('Sliding client\'s window ' + str(number) + ' position(s)')             
            self.lower += number
            self.upper += number
            self.sendPacket(self.upper)

    def slideWindow(self):
        i = self.lower
        while i <= self.upper:
            if self.packetList[i].getAckRcvd() is True:
                self.slideWindowBy(1)                        
            else:
                break
            i += 1
    
    def recieveAck(self):
        while True:
            self.debug('Recieving ACK...')
            ack = None
            self.sock.settimeout(0.2)
            try:
                ack = self.sock.recv(5)
                if ack is not None:
                      self.packetList[int(ack)].setAckRcvd(True)
                self.checkTime()  
                self.slideWindow()
                if int(ack) == 10001 : break
                self.debug('Recieved ACK message for packet '+ack)
            except socket.timeout, e: pass
            self.sock.settimeout(None)
            

    def runClientNode(self,filename):
        self.connect()
        self.readFromFile(filename)
        self.sendWindow()
        self.recieveAck()            

class Server(Node):
    def __init__(self, mode, port, timeout, windowSize, name):
        super(Server, self).__init__(mode, port, name)
        self.packetList = [None]*100
        self.upper      = windowSize - 1
        self.lower      = 0
        self.windowSize = windowSize
        self.timeout    = timeout        
        print 'Server node started'

    def exportResults(self):
        result = ""
        for x in self.packetList:
            result += x.getCharacter()
        with('result.txt','w') as f:
            f.write(result)
    
    def recieve(self):
        cont = True
        while cont:              
            self.debug('Waiting connection from middle node...')
            connection, address = self.sock.accept()
            try:
                while True:      
                    buf = connection.recv(7)
                    if buf:                            
                        seqNumber, character = buf.split(':', 1)
                        if seqNumber=='' or int(seqNumber) == 10001: 
                            cont = False
                            break
                        print 'Recieved: '+ buf
                        if self.packetList[int(seqNumber)] is None:
                                  self.packetList[int(seqNumber)] = Packet(buf)
                        connection.send(seqNumber)
                    else: break                       
            finally:
                connection.close()
                # self.exportResults()

    def runServerNode(self):
            self.bind()
            self.listen()
            self.recieve()

class Middle(Node):   #proba
    def __init__(self, mode, port, queue1, queue2, probability, name):
        super(Middle, self).__init__(mode, port, name)
        self.sock     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.qSend    = queue1
        self.qRecieve = queue2
        self.prob     = probability
    
    def recieveFromClient(self):
        cont = True
        while cont:              
                self.debug('Waiting for connection from client...')
                connection, address = self.sock.accept()
                try:
                    while True:
                        buf = None 
                        connection.settimeout(0.2)
                        try:
                            buf = connection.recv(7)
                        except socket.timeout, e: pass  
                        connection.settimeout(None)   
                        if buf is not None:  #if there IS a message         
                            print self.name+'Recieved: '+ buf                  
                            self.putData(buf) #puts recieved message onto sendQueue                
                        self.debug('Retrieving ACK message from server to client...')
                        ack = self.getData()
                        if ack is not None: #checks if there's an ACK waiting to be forwarded
                            if ack =='' or int(ack) == 10001: 
                                cont = False
                                break
                            print self.name +'Retrieved. Forwarding ACK:['+ack+'] to client'
                            connection.sendall(str(ack)) #send it
                        else:
                            print self.name + 'No ACK to forward right now.' #if not, notify                  
                        #break     #break                   
                finally:
                    connection.close() 

    def runClientMiddle(self):
        self.bind()
        self.listen()
        self.recieveFromClient()

    def recieveFromMiddle(self):
        while True:
            packet = self.getData()
            if packet != None:
                self.debug('Sending '+packet+' to server...')
                self.sock.send(packet)
                self.debug('Waiting for server\'s answer...')
                ack = self.sock.recv(5)
                self.debug('Recieved '+ack+' from server')
                self.putData(ack)

    def runMiddleServer(self):
        self.connect()
        self.recieveFromMiddle()

    def getData(self, recieveLock=None):
        #recieveLock.acquire()
        if not self.qRecieve.empty():                               #if queue is not empty
            data = self.qRecieve.get()                              #gets value from queue
            #self.debug(+"Retrieved "+str(data)+" from queue")    #debug
            #recieveLock.release()          
            return data                                             #return item from queue
        else:          
            #recieveLock.release()          
            #self.debug("Nothing to retrieve, empty queue.")                #debug (empty queue)
                
            pass
        
    def putData(self, data, sendLock=None):
        #data = self.sock1.recv(1024)                   #descomentar esto para recibir del socket y quitar el parametro
        #if data is not None:                           #if recieved data is not None, send data
        #######if random.uniform(0,1) > self.prob:     #proba
        #####sendLock.acquire()
        if self.mode is 1:  print self.name+ "Sending "+data+" through queue..."    #debug  
        self.qSend.put(data)                            #puts in queue
        if self.mode is 1:  print self.name+ "Sent!"    #debug

        #####sendLock.release()
