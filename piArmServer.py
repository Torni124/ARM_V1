import socket
from time import sleep
host = ''
port = 5560

import ikpy.utils.plot as plot_utils
import numpy as np
import time
import math
import ipywidgets as widgets
import serial
from time import sleep
import RPi.GPIO as gpio
from gpiozero import Servo
import ikpy.chain


error = .05 # in meters

direction_pin = 20
pulse_pin = 21
cw_direction = 0
ccw_direction = 1

bdp = 20
bsp = 21

adpl = 15
aspl = 14

adpnl = 18
aspnl = 23

a2dp = 25
a2sp = 24

rp =7
ep = 8
cp = 12


# Angles of Each Motor

baseActual = 0
oneActual = 45
twoActual = 135
spinActual = 0
endActual = 0


gpio.setmode(gpio.BCM)
gpio.setup(bdp, gpio.OUT)
gpio.setup(rp, gpio.OUT)
gpio.setup(ep, gpio.OUT)
gpio.setup(cp, gpio.OUT)

gpio.setup(bsp, gpio.OUT)
gpio.setup(adpl, gpio.OUT)
gpio.setup(aspl, gpio.OUT)
gpio.setup(adpnl, gpio.OUT)
gpio.setup(aspnl, gpio.OUT)
gpio.setup(a2dp, gpio.OUT)
gpio.setup(a2sp, gpio.OUT)

pwmr=gpio.PWM(rp,50)
pwmr.start(0)
pwme = gpio.PWM(ep, 50)
pwme.start(0)
pwmc = gpio.PWM(cp, 50)
pwmc.start(0)

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

def runTxtCommands(conn, array):
    while True:
        data = conn.recv(1024)
        data = data.decode('utf-8')
        if(data == "stop"):
             global stop
             stop = True
             conn.sendall(str.encode("Stopping"))
             return
        coords = data.split(" ")
        x = coords[0]
        y = coords[1]
        z = coords[2]
        newPoint = np.array([x,y,z])
        inputPositions = np.r_[inputPositions, [newPoint]]
        print(coords)
        angles = singleKinematics(newPoint)
        checkError(newPoint, angles)
        reply = "Received " + x + " " + y + " " + z + " starting motion"
        conn.sendall(str.encode(reply))
        moveAll(angles[0], angles[1], angles[2], angles[3], angles[4])
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


def moveAll(bAngle, oneAngle, twoAngle,spinAngle, endAngle):
     # Remember to catch edge case if < 0 or > 180
     # And limits for all motors, if hit limit set to max in that direction? 
     # WHAT ARE THE LIMITS???? UPDATE
     # Make sure works for positive and negative, problems are probably in setting bMove if less then zero
     global baseActual, oneActual, twoActual, spinActual, endActual
     bMove = bAngle- baseActual 
     oneMove = oneAngle - oneActual
     twoMove = twoAngle - twoActual
     #print("Actuals: ", baseActual)
     #print("Base: ", bMove, " One: ", oneMove, " Two: ", twoMove)
     baseActual += bMove
     if(baseActual > 180):
         bMove = 180-baseActual + bAngle
         baseActual =180
     elif(baseActual < -180):
         bMove = -180 - baseActual + bAngle
         baseActual = -180

     oneActual += oneMove
     if(oneActual > 45):
          oneMove = 45 - oneActual + oneAngle
          oneActual = 45
     elif(oneActual < -90):
        oneMove = -90 - oneActual + oneAngle
        oneActual = -90

     twoActual += twoMove
     if(twoActual > 135):
          twoMove = 135 - twoActual + twoAngle
          twoActual = 135
     elif(twoActual < -90):
        twoMove = -90 - twoActual + twoAngle
        twoActual = -90

     spinActual = spinAngle
     if(spinActual > 90):
          spinActual = 90
     elif(spinActual < -90):
        spinActual = -90

     endActual = endAngle
     if(endActual > 90):
          endActual = 90
     elif(endActual < -90):
        endActual = -90
     moveSteppers(bMove, oneMove, twoMove)
     moveServos(spinActual, endActual)
     
def moveServos(sAngle, eAngle):
     
     # Adjusting from -90 to 90 to 0-180 is this necessary? 
     # CHECK RANGE OF SERVOS
    
     spinAngle = sAngle + 90
     endAngle = eAngle + 90
     print(endAngle)
     spinAngle = 147
     outr = spinAngle/18 + 2.5
     oute = endAngle/18 + 2.5
     gpio.output(rp, True) 
     pwmr.ChangeDutyCycle(outr)
     sleep(1)
     gpio.output(rp, False)
     pwmr.ChangeDutyCycle(0)
     gpio.output(ep, True) 
     pwme.ChangeDutyCycle(oute)
     sleep(1)
     gpio.output(ep, False)
     pwme.ChangeDutyCycle(0)


def moveSteppers(bAngle, oneAngle, twoAngle):
    # Add angle -> steps conversion 
    bStep = bAngle * 4.69444
    oneStep = oneAngle * 12.7778
    twoStep = twoAngle* 11.22222
    # Direction determining 
    if(bStep < 0):
        bDir = False
        bStep = abs(bStep)
    else: 
        bDir = True
    if(oneStep < 0):
        oneDir = False
        oneStep = abs(oneStep)
    else: 
        oneDir = True
    if(twoStep < 0):
        twoDir = False
        twoStep = abs(twoStep)
    else: 
        twoDir = True


    #  Direction setting 
    # check for proper directions 
    if(bDir == True):
            gpio.output(bdp, gpio.LOW)
    else:
            gpio.output(bdp, gpio.HIGH)
    if(oneDir == True):
            gpio.output(adpl, gpio.LOW)
            gpio.output(adpnl, gpio.LOW)
    else:
            gpio.output(adpl, gpio.HIGH)
            gpio.output(adpnl, gpio.HIGH)
    if(twoDir == True):
            gpio.output(a2dp, gpio.LOW)
    else:
            gpio.output(a2dp, gpio.HIGH)

   # TODO: Add direction code for servos      
            
    list = [bStep, oneStep, twoStep]
    maxStep = int(max(list))
    for x in range(maxStep):
        #Base
        # IS THIS CUTTING ONE STEP? > vs >=
        if(bStep > x):
            gpio.output(bsp, gpio.HIGH)
            sleep(.001)
            gpio.output(bsp, gpio.LOW)
            sleep(.001)
        if(oneStep > x):
            gpio.output(aspl, gpio.HIGH)
            gpio.output(aspnl, gpio.HIGH)
            sleep(.001)
            gpio.output(aspl, gpio.LOW)
            gpio.output(aspnl, gpio.LOW)
            sleep(.001)          
        if(twoStep> x):
            gpio.output(a2sp, gpio.HIGH)
            sleep(.001)
            gpio.output(a2sp, gpio.LOW)
            sleep(.001)            
def singleKinematics(x, y, z):
     target_position = [x, y, z]
     ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
     #print("The angles of each joints are : ", list(map(lambda r:math.degrees(r),ik.tolist())))
     baseangle = math.degrees(ik[1])
     armoneangle = math.degrees(ik[2])
     armtwoangle = math.degrees(ik[3])
     spin = math.degrees(ik[4])
     armthreeangle = math.degrees(ik[5])
     angles = [baseangle, armoneangle, armtwoangle, spin, armthreeangle]
     return angles

def checkError(position, angles):
         anglesCompute = [0, math.radians(angles[0]),  math.radians(angles[1]), math.radians(angles[2]), math.radians(angles[3]), math.radians(angles[4])]
         computePosition = my_chain.forward_kinematics(anglesCompute)
         xGood = abs(computePosition[0] - position[0]) > error
         yGood = abs(computePosition[1] - position[1]) > error
         zGood = abs(computePosition[2] - position[2]) > error
         if(xGood and yGood and zGood):
              return
         else:
              errorMessage = "Inaccurate final position, "
              if(not xGood):
                   errorMessage += " x value is inaccurate by " + abs(position[0]-computePosition[0])
              if(not yGood):
                   errorMessage += " y value is inaccurate by " + abs(position[1]-computePosition[1])
              if(not zGood):
                   errorMessage += " z value is inaccurate by " + abs(position[2]-computePosition[2])
              conn.sendall(str.encode(errorMessage))  
              raise ValueError(errorMessage)


######################################################################################

my_chain = ikpy.chain.Chain.from_urdf_file("armfour.urdf",active_links_mask=[False, True, True, True, True, True])
target_orientation = [0, 0, 1]

s = setupServer()
mode = setMode()

inputPositions = np.empty([0, 3])
finalInputArray = np.empty([1,3]) 
stop = False
while stop == False:
    try:
        conn = setupConnection()
        if(mode == "txt"):
            #print("in txt")
            finalInputArray = runTxtCommands(conn, inputPositions)
        else:
            dataTransfer(conn)
    except:
        break
print(finalInputArray)
        
returns = bool(input("return to default start?"))
if(returns == True):
    moveAll(0, 45, 135, 90, 90)
gpio.cleanup()
print("GPIO off, all motions complete")



#computed_position = my_chain.forward_kinematics(ik)
#print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
#print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])





