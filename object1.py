import socket
import threading
import os

def ReadFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("Exists " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'ok':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR")
        
    sock.close()
    
def Main():
    host = '127.0.0.1'
    port = 5000
    
    print "Hola!"
    
    s = socket.socket()
    s.bind((host,port))
    
    s.listen(5)
    
    print "Server Started"
    
    while True:
        c, addr = s.accept()
        print "client connected ip: " + str(addr)
        t = threading.Thread(target=ReadFile, args=("retrThread", c))
        t.start()
    
    s.close()
    
if __name__ == '__main__':
    Main()