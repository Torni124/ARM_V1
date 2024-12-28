import socket
import numpy as np 
host = '192.168.1.21' # get ip of pi
port = 5560
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s
def sendReceive(s, message):
    s.send(str.encode(message))
    reply = s.recv(1024)
    #print("Reply Recieved")
    #print("Disconnecting")
    s.send(str.encode("EXIT"))
    s.close()
    reply = reply.decode('utf-8')
    return reply
def transmit(message):
    s = setupSocket()
    response = sendReceive(s, message)
    return response 
def sendPositions(positions):
    for x in positions.len():
        coords = positions[x]
        stringCoords = str(coords)
        response = transmit(stringCoords)
        return response

def loadTxtData(file):
    positions = np.loadtxt(file, delimiter=",")
    return positions

def assembleData():
    done = False
    positions = np.empty([0,4])
    while (done==False):
        x = input("X: ")
        if(x == "end"):
            return positions
        x = int(x)
        y= int(input("Y: "))
        z = int(input("Z: "))
        newPoint = np.array([x,y,z])
        positions = np.r_[positions, [newPoint]]
        sendPosition = input("Send the command?(y/n)")
        if(sendPosition == "y"):
            response = transmit(str(newPoint))
            print(response)
    return positions


def txtSend(array):
    try:
        for row in array:
            print(row)
            rowStr = str(row).strip("[]")
            rowStr = rowStr.split()
            sendData = ' '.join(rowStr)
            print(sendData)
            response = transmit(sendData)
            if(response == "fail"):
                print("failed on command " + sendData)
                break
            print(response)
    except KeyboardInterrupt:
        response = transmit("stop")
        print(response)


#command = input("Enter message")
#response = transmit(command)
#print(response)
file = r"C:\Users\tbodi\Downloads\armangles.txt"

while (True):
    mode = input("\"txt\" for txt file, \"manual\" for individual input")
    if(mode == "txt"):
        response = transmit("txt")
        print(response)
        dataType = input("Angles(a) or Coords(c)?")
        if(dataType == "a"):
            response = transmit("angle")
        else:
            response = transmit("coords")
        print(response)
        if(len(file)> 0):
            print("Retriving data from " + file)
            positions = loadTxtData(file)
            print("Data retrived")
        else:
            file = input("Input file location")
            print("Drawing data from " + file)
            positions = loadTxtData(file)
            print("Data retrived")
        display = input("Would you like to print out the array? (y/n)")
        if(display == "y"):
            print(positions)
        sendData = input("Send the commands?(y/n)")
        if(sendData == "y"):
            txtSend(positions)
        break
    elif(mode == "manual"):
        positions = assembleData()
        break
    else:
        print("Invalid input")

response = transmit("stop")
print(response)
print("Program complete")



        

"""
while True:
    command = input("Enter command")
    if command == 'EXIT':
        # send exit
        s.send(str.encode(command))
        break
    elif command == 'KILL':
        s.send(str.encode(command))
        break
    s.send(str.encode(command))
    reply = s.recv(1024)
    print(reply.decode('utf-8'))

s.close() """