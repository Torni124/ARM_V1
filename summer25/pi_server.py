import socket
from time import sleep
host = ''
port = 5560

storedValue = "Hello"

def setupServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("created")
	try:
		s.bind((host, port))
	except socket.error as msg:
		print (msg)
	print("Bound")
	return s
def setupConnection():
	s.listen(1) # Allows 1 connection at a time
	conn, address = s.accept()
	print("Connected to: " + address[0] + ":" + str(address[1]))
	return conn

def GET():
	reply = storedValue
	return reply

def REPEAT (dataMessage):
	reply = dataMessage[1]
	return reply	
def runTxtCommands(conn):
    while True:
        data = conn.recv(1024)
        data = data.decode('utf-8')
        coords = data.split(" ")
        x = coords[0]
        y = coords[1]
        z = coords[2]
        reply = "Received " + x + " " + y + " " + z
        conn.sendall(str.encode(reply))
        print(coords)
        break
    conn.close()

def dataTransfer(conn):
    while True:
        data = conn.recv(1024)
        data = data.decode('utf-8')
        reply = "received " + data
        conn.sendall(str.encode(reply))
        print(data + " sent")
        break
    conn.close()
    
def setMode():
    while True:
        conn = setupConnection()
        while True:
            data = conn.recv(1024)
            data = data.decode('utf-8')
            if(data == "txt"):
                reply = "set mode to txt"
                conn.sendall(str.encode(reply))
                return "txt"
            else:
                reply = "manual mode"
                conn.sendall(str.encode(reply))
                return "man"
s = setupServer()
mode = setMode()
while True:
    try:
        conn = setupConnection()
        if(mode == "txt"):
            print("in txt")
            runTxtCommands(conn)
        else:
            dataTransfer(conn)
    except:
        break
