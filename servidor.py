# from object1 import Server

# def run(debug, port, timeout, winSize):
#       server = Server(debug, port, timeout, winSize,'[SERVER]:')
#       server.runServerNode()

# if __name__ == '__main__':
#       deb = input("Set debug state [1=debug mode/0=standard mode]: ")
#       por = input("Set port to bind with: ")
#       time  = input("Set timeout value: ")
#       win = input("Set window size: ")
#       run(deb, por, time, win)

from object1 import Server

def run():
      server = Server(1,10001,1,5,'[SERVER]:')
      server.runServerNode()

if __name__ == '__main__':
      run()