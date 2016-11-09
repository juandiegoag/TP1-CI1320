# from object1 import Client

# def runClient(debug, port, timeout, window, filename):
#       client = Client(debug, port , timeout, window,'[CLIENT]:')
#       client.runClientNode(filename)

# if __name__ == '__main__':
#       dbg = input("Set debug state [1=debug mode/0=standard mode]: ")
#       prt = input("Set client communication port: ")
#       tmout  = input("Set timeout value in seconds: ")
#       winSize = input("Set window size: ")
#       filename = raw_input("Set file to read: ")

#       runClient(dbg, prt, tmout, winSize, filename)

from object1 import Client

def runClient():
      client = Client(1,10000,0.15,5,'[CLIENT]:')
      client.runClientNode('prueba.txt')

if __name__ == '__main__':
      runClient()