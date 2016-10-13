from object1 import Client

def run():
      client = Client(1,10000,1,5)
      client.connect()
      client.readFromFile('prueba')
      client.sendWindow()
      while True:
            client.recieveAck()

if __name__ == '__main__':
      run()