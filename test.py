import time
import Queue
import threading
import object1

def run():
      #Middle thread
      m = object1.Middle(debug, 5000,5500, q1, q2, 10)
      
      i = 0
      while i < 200:
            #print name + " getting data"
            item = m.getData(l1)
            if item != None:
                  print name + " recieved " + str(item) + str(i)
                  i += 1
            m.putData(l2, item)
            
      print name +" End"
      exit(0)
      
      


    
if __name__ == '__main__':
      debug      = input("Set debug state [1=debug mode/0=standard mode]: ")
      winSize    = input("Set window size: ")
      queue1 = Queue.Queue(winSize)
      queue2 = Queue.Queue(winSize)
      queue1.put("inicio")
      queue2.put("inicio")
      lock1 = threading.Lock()
      lock2 = threading.Lock()
      name1 = "thread 1: "
      name2 = "thread 2: " 
      
      t1 = threading.Thread(target=run, args=(debug, queue1, queue2, lock1, lock2, name1))
      t2 = threading.Thread(target=run, args=(debug, queue2, queue1, lock2, lock1, name2))
      
      t1.start()
      t2.start()
