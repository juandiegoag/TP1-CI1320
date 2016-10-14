from object1 import Middle
import threading
import Queue

def run1(debug, por, q1, q2, prob,kill):
      #From client to middle
      m = Middle(debug, por,q1, q2, prob,'[CLIENT-MIDDLE]:',kill)
      m.runClientMiddle()

def run2(debug, por, q1, q2, prob,kill):
      #From middle to server
      m = Middle(debug, por, q1, q2, prob,'[MIDDLE-SERVER]:',kill)
      m.runMiddleServer()         
      


    
if __name__ == '__main__':
      debug      = input("Set debug state [1=debug mode/0=standard mode]: ")      
      kill      = input("Do you want to kill packets?(only in debug mode)[1=yes/0=no]: ")
      portClient = input("Set the port for the client to connect(must be the same port the client uses): ")
      portServer = input("Set the port binded with the server (must be the same port the server uses): ")
      prob       = input("Set packet loss probability[0.0 - 1.0]: ")
      winSize    = input("Set window size (same as client and server window):")
      
      
      queue1 = Queue.Queue(winSize)
      queue2 = Queue.Queue(winSize)

      t1 = threading.Thread(target=run1, args=(debug, portClient, queue1, queue2, prob,kill))
      t2 = threading.Thread(target=run2, args=(debug, portServer, queue2, queue1, prob,kill))
      
      t1.start()
      t2.start()
# from object1 import Middle
# import threading
# import Queue
# def run1(debug, q1, q2):
#       #From client to middle
#       m = Middle(debug, 10000,q1, q2, 0.05,'[CLIENT-MIDDLE]:')
#       m.runClientMiddle()

# def run2(debug, q1, q2):
#       #From middle to server
#       m = Middle(debug, 10001, q1, q2, 0.05,'[MIDDLE-SERVER]:')
#       m.runMiddleServer()         
      


    
# if __name__ == '__main__':
#       queue1 = Queue.Queue(5)
#       queue2 = Queue.Queue(5)

#       t1 = threading.Thread(target=run1, args=(1, queue1, queue2))
#       t2 = threading.Thread(target=run2, args=(1, queue2, queue1))
      
#       t1.start()
#       t2.start()
