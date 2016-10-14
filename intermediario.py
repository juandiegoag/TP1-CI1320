from object1 import Middle
import threading
import Queue
def run1(debug, q1, q2):
      #From client to middle
      m = Middle(debug, 10000,q1, q2, 0.2,'[CLIENT-MIDDLE]:')
      m.runClientMiddle()

def run2(debug, q1, q2):
      #From middle to server
      m = Middle(debug, 10001, q1, q2, 0.2,'[MIDDLE-SERVER]:')
      m.runMiddleServer()         
      


    
if __name__ == '__main__':
      queue1 = Queue.Queue(5)
      queue2 = Queue.Queue(5)

      t1 = threading.Thread(target=run1, args=(1, queue1, queue2))
      t2 = threading.Thread(target=run2, args=(1, queue2, queue1))
      
      t1.start()
      t2.start()
 
