import time

import object1

def run():
      #system variables
      ddebug      = input("Set debug state [1=debug mode/0=standard mode]: ")
      winSize    = input("Set window size: ")
      s = object1.Server(0, 5000, 3, winSize)
      #s.listen()
      time.sleep(1)
      c = object1.Client(0, 5000, 3, winSize)
      #s.recieve()
      #c.send()
      
      


    
if __name__ == '__main__':
    run()