from object1 import Client

def runClient():
      client = Client(1,10000,5,5,'[CLIENT]:')
      client.runClientNode('prueba.txt')

if __name__ == '__main__':
      runClient()