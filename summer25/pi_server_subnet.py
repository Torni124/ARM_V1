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
def dataTransfer(conn):
	#Loop that sends and recvies until stopper
	
	while True:
		#Recieve
		data = conn.recv(1024)
		data = data.decode('utf-8')
		# splits data to seperate command from data
		"""dataMessage = data.split(' ', 1)
		command = dataMessage[0]
		if command == 'GET':
			reply = GET()
		elif comand == 'REPEAT':
			reply = REPEAT(dataMessage)
		elif command == 'EXIT':
			print("Client disconnected")
			
		elif command == 'KILL':
			print("Shut down command received")
			s.close()
			break
		else:
			reply = 'Unknown Command'
		#Send reply"""
		sleep(1)
		reply = "Recieved " + data
		conn.sendall(str.encode(reply))
		print("Data sent")
		print(data)
		break
	conn.close()
s = setupServer()

while True:
	try:
		conn = setupConnection()
		dataTransfer(conn)
	except:
		break
