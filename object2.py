import socket

def Main():
    host = '127.0.0.1'
    port = 5000
    
    print "Adios"
    
    s = socket.socket()
    s.connect((host,port))
    
    filename = raw_input("Filename: ")
    if filename != 'q':
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'Exists':
            filesize = long(data[6:])
            message = raw_input("file of " + str(filesize) + "bytes, download? Y/N\n")
            if message == 'Y' or message == 'y':
                s.send('ok')
                f = open('new_' +filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                print "Complete"
        else:
            print "File does not exist"
    
    s.close()
    
if __name__ == '__main__':
    Main()