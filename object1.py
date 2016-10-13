import socket
import sys
import threading
import os
import time

#Single packet representation class.
class Packet(object):
    def __init__(self, seqNumber, character):
        self.seqNumber  = seqNumber
        self.character  = character
        self.serialized = str(seqNumber)+":"+str(character)
        self.ackRecvd   = False
        self.sent       = time.time()
    
    def __init__(self, serializedString):
        self.seqNumber, self.character = serializedString.split(':', 1)
        self.seqNumber = int(self.seqNumber)
        self.serialized = serializedString
    
    def getSerialized(self):
        return self.serialized
    
    def getAckRcvd(self):
        return self.ackRcvd
    
    def setAckRcvd(self, rcv):
        self.ackRecvd = rcv
    
    def send(self):
        self.sent = time.time()

    def getSent(self):
        return self.sent

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

    def bind(self , portToBind):
        bindAddress = ('localhost',self.port)
        self.sock.bind(bindAddress)
    
    def closeSocket(self):
        self.sock.close()
                                 
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
        if self.mode is 1:
            print 'Reading and parsing from file into list'
        with open(filename) as f:
            counter = 0
            while True:
                readChar = f.read(1)
                if not readChar:
                    break
                counter += 1 
                self.packetList.append(packet(counter,readChar))
        if self.mode is 1:
            print 'Reading done. Total '+str(len(self.packetList))+' nodes to send.'

    def sendPacket(self, index):
        packet = packetList[index].getSerialized()
        if self.mode is 1:
                  print 'Sending packet: ' + packet + ' to server' 
        packetList[index].send()
        self.sock.send(packet)
    
    def checkTime(self):
        i = self.lower
        while i <= self.upper:
            if self.packetList[i].getSent()+timeout > time.time():
                self.sendPacket(i)

    def sendWindow(self):
        i = self.lower
        while i <= self.upper:
            self.sendPacket(i)
            i += 1

    def slideWindow(self, number):
         if self.mode is 1:
                  print 'Sliding window ' + str(number) + ' position(s)'             
        self.lower += number
        self.upper += number
    
    def recieveAck(self):
        if self.mode is 1:
            print 'Recieving ACK...'
        ack = self.sock.recv(1)
        if ack:
            if self.mode is 1:
                print 'Recieved ACK message for packet '+str(self.lower+int(ack))
            self.packetList[self.lower+int(ack)].setAckRcvd(True)  
            if ack is 0:
                self.slideWindow(1)
            i = self.lower
            while i < self.upper:
                if packetList[i].getAckRcvd() is True:
                    self.slideWindow(1)                        
                else:
                    break
                i += 1
            

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
        self.packetList = []
        self.upper = windowSize - 1
        self.windowSize = windowSize
        self.timeout    = timeout        
        self.windowSize = windowSize
        print 'Server node started

    def recieve(self):
        try:
            while True:              
                if self.mode is 1:
                    print 'Waiting to connect'
                connection, address = sock.accept()
                buf = connection.recv(7)
                if buf:
                    print buf

                    seqNumber, character = buf.split(':', 1)
                    connection.send(str(int(seqNumber)%8))                       
                    break
        finally:
            connection.close()





class Middle(Node):#proba
    def __init__(self, mode, clientPort, serverPort):
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


