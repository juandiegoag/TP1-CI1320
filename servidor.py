from object1 import Server

def run():
      server = Server(1,10000,1,5)
      server.bind()
      server.listen()
      server.recieve()

if __name__ == '__main__':
      run()
