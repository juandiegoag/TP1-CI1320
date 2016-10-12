import object1
import time

def run():
      #system variables
    #debug      = input("Set debug state [1=debug mode/0=standard mode]: ")
    winSize    = input("Set window size: ")
    
    timeout = float(input("Timeout en ms: "))
    timeout = float(timeout/1000)   #pasa ms a segundos (float)
    lista = [0]*winSize             #timeouts por paquete de la ventana
    estado = [False]*winSize        #si cada espacio de la ventana recibio ACK
    
    print timeout
      
    for i in range(0,winSize):      #llena array con el tiempo en que envia el paquete
        #lista[i] = time.clock()
        print "enviando paquete por primera vez: " + str(i)
        lista[i] = time.time()
        #time.sleep(timeout)
    
    print "-------------------------"
    print""
    print""
    print""
    
    tiempo = time.time()            #verifica que que no haya terminado el timeout
    while time.time() < tiempo + timeout:
        for i in range(0, winSize):
            if lista[i] + timeout > time.time() and estado[i] == False: #mientra no haya llegado ACK y no haya terminado el timeout
                #print "algo"
                #se llega paquete: estado[i] = True
                pass
            else:       #termino timeout
                print "timeout terminado, enviando paquete " + str(i)
                #reenvia paquete
                estado[i] = True
        
    print "-------------------------"
    
    #for i in range(0, winSize):
    #    print estado[i]
    
    for i in range(0, winSize): #reenvia paquetes que faltan
        if estado[i] == False:
            print "enviando paquete " + str(i)

    
if __name__ == '__main__':
    run()