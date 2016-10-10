import socket
import sys
import threading
import os

#Single packet representation class.
class Packet(object):
    def __init__(self, seqNumber, character):
        self.seqNumber  = seqNumber
        self.character  = character
        self.serialized = seqNumber+":"+character
        self.status     = True #True means that the packet is NOT declined 
    
    def unserialize(self, serializedString):
        self.seqNumber, self.character = serializedString.split(':', 1)
        self.serialized = serializedString
        self.status = True

#Node representation. Superclass containing server, middle, and client.     
class Node(object):
   def __init__(self, mode, port):
        self.mode         = mode
        self.port         = port
        #TCP/IP socket for use:
        self.sock         = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        connectAddress = ('localhost',self.port)
        self.sock.connect(connectAddress)

    def bind(self , portToBind):
        bindAddress = ('localhost',self.port)
        self.sock.bind(bindAddress)
                                 
class Client(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super().__init__(mode, port)
        self.packetList = []
        self.timeout    = timeout
        self.windowSize = windowSize  

    def readFromFile(self, filename):
        with open(filename) as f:
            counter = 0
            while True:
                readChar = f.read(1)
                if not readChar:
                    break
                counter += 1 
                self.packetList.append(packet(counter,readChar))

    def send(self):
        
              
    def sendAck(self):
              

class Server(Node):
    def __init__(self, mode, port, timeout, windowSize):
        super().__init__(mode, port)
        self.packetList = []
        self.timeout    = timeout
        self.windowSize = windowSize       



class Middle(Node):
#proba


# def ReadFile(name, sock):
#     filename = sock.recv(1024)
#     if os.path.isfile(filename):
#         sock.send("Exists " + str(os.path.getsize(filename)))
#         userResponse = sock.recv(1024)
#         if userResponse[:2] == 'ok':
#             with open(filename, 'rb') as f:
#                 bytesToSend = f.read(1024)
#                 sock.send(bytesToSend)
#                 while bytesToSend != "":
#                     bytesToSend = f.read(1024)
#                     sock.send(bytesToSend)
#     else:
#         sock.send("ERR")
        
#     sock.close()
    
# def Main():
#     host = '127.0.0.1'
#     port = 5000
    
#     print "Hola!"
    
#     s = socket.socket()
#     s.bind((host,port))
    
#     s.listen(5)
    
#     print "Server Started"
    
#     while True:
#         c, addr = s.accept()
#         print "client connected ip: " + str(addr)
#         t = threading.Thread(target=ReadFile, args=("retrThread", c))
#         t.start()
    
#     s.close()
    
# if __name__ == '__main__':
#     Main()