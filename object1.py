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
        self.sent       = time.time()
    
    def getSerialized(self):
        return self.serialized
    
    def getAckRcvd(self):
        return self.ackRecvd
    
    def setAckRcvd(self, rcv):
        self.ackRecvd = rcv
    
    def send(self):
        self.sent = time.time()

    def getSent(self):
        return self.sent
    
    def getCharacter(self):
        return self.character

#Node representation. Superclass containing server, middle, and client.     
class Node(object):
    def __init__(self, mode, port):
        self.mode         = mode #1 for debug, 0 for standard
        self.port         = port
        #TCP/IP socket for use:
        self.sock         = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        connectAddress = ('localhost',self.port)
        self.sock.connect(connectAddress)

    def bind(self):
        bindAddress = ('localhost',self.port)
        self.sock.bind(bindAddress)
        print ('Server binded to', bindAddress)

    def closeSocket(self):
        self.sock.close()
    
    def listen(self):
        self.sock.listen(1)
                                            
class Client(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super(Client,self).__init__(mode, port)
        self.packetList = []
        self.lower = 0 #lower and upper to handle sliding window
        self.upper = windowSize - 1
        self.windowSize = windowSize
        self.timeout    = timeout
        print 'Client node started'

    def readFromFile(self, filename):
        if self.mode is 1: print 'Reading and parsing from file into list'
        with open(filename) as f:
            seqNumber = 0
            while True:
                readChar = f.read(1)
                if not readChar:
                    break
                seqNumber += 1 
                sequenceNumber = str(seqNumber) #normalize all possible numbers
                if len(str(seqNumber))   is 1: sequenceNumber = "0000"+str(seqNumber)
                elif len(str(seqNumber)) is 2: sequenceNumber = "000" +str(seqNumber)
                elif len(str(seqNumber)) is 3: sequenceNumber = "00"  +str(seqNumber)
                elif len(str(seqNumber)) is 4: sequenceNumber = "0"   +str(seqNumber)
                serialized = sequenceNumber+":"+str(readChar)

                self.packetList.append(Packet(serialized))
        if self.mode is 1: print 'Reading done. Total '+str(len(self.packetList))+' nodes to send.'

    def sendPacket(self, index):
        packet = self.packetList[index].getSerialized()
        if self.mode is 1: print 'Sending packet: ' + packet + ' to server' 
        self.packetList[index].send()
        self.sock.send(packet)
    
    def checkTime(self):
        i = self.lower
        while i <= self.upper:
            if self.packetList[i].getAckRcvd is False and self.packetList[i].getSent()+timeout > time.time():
                self.sendPacket(i)

    def sendWindow(self):
        i = self.lower
        while i <= self.upper:
            self.sendPacket(i)
            i += 1

    def slideWindowBy(self, number):
        if self.mode is 1:
            print 'Sliding client\'s window ' + str(number) + ' position(s)'             
        if self.upper+1 < len(self.packetList):
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
        if self.mode is 1: print 'Recieving ACK...'
        ack = self.sock.recv(1)
        if self.mode is 1: print 'Recieved ACK message for packet '+str(self.lower+int(ack))
        self.packetList[self.lower+int(ack)].setAckRcvd(True)  
        # self.checkTime()
        # if ack is 0: self.slideWindowBy(1)
        self.slideWindow()
            

    # def checkAllAcks(self):
    #     if any(ack == False for ack in self.ackArray) is False:
    #         falses = (i for i,x in enumerate(self.ackArray) if x is False)
    #         minWindow = min(falses)
    #         self.lower += minWindow
    #         self.upper += minWindow
    #         for i in falses:
    #             self.sendPacket(self.lower+i)
    #     else:
    #         self.lower += self.windowSize
    #         self.upper += self.windowSize
              

class Server(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super(Server, self).__init__(mode, port)
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
        while True:              
            if self.mode is 1: print 'Waiting to connect...'
            connection, address = self.sock.accept()
            try:
                while True:      
                    buf = connection.recv(7)
                    print 'Recieved: '+ buf
                    if buf:                            
                        seqNumber, character = buf.split(':', 1)
                        if self.packetList[int(seqNumber)] is None:
                            self.packetList[int(seqNumber)] = Packet(buf)
                        connection.send(str(int(seqNumber) % self.windowSize ))
                    else: break                       
            finally:
                connection.close()
                # self.exportResults()

class Middle(Node):   #proba
    def __init__(self, mode, clientPort, serverPort, queue1, queue2, probabilidad):
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.qSend = queue1
        self.qRecieve = queue2
        self.proba = probabilidad
    
    def getData(self, recieveLock):
        recieveLock.acquire()
        if not self.qRecieve.empty():
            data = self.qRecieve.get()
            recieveLock.release()
            self.sock.send(data)
        else:
            recieveLock.release()
        
    def putData(self, sendLock):
        data = self.sock1.recv(1024)
        if random.uniform(0,1) > self.proba:
            sendLock.acquire()
            self.qSend.put(data)
            sendLock.release()