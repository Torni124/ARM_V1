from time import sleep
import RPi.GPIO as gpio
from gpiozero import Servo
 
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

servo = Servo(7)

gpio.setmode(gpio.BCM)
gpio.setup(bdp, gpio.OUT)

gpio.setup(bsp, gpio.OUT)
gpio.setup(adpl, gpio.OUT)
gpio.setup(aspl, gpio.OUT)
gpio.setup(adpnl, gpio.OUT)
gpio.setup(aspnl, gpio.OUT)
gpio.setup(a2dp, gpio.OUT)
gpio.setup(a2sp, gpio.OUT)

gpio.output(direction_pin, cw_direction)
def armTwo(s, d):
    for x in range(s+1):
        if(d == True):
            gpio.output(a2dp, gpio.HIGH)
        else:
            gpio.output(a2dp, gpio.LOW)
            
        gpio.output(a2sp, gpio.HIGH)
        sleep(.001)
        gpio.output(a2sp, gpio.LOW)
        sleep(.001)


def moveBoth(bs, bd, sa, ad):
    high = 0
    low = 1000000000
    
    if(bs < sa):
        high = sa
        low = bs
    else :
        high = bs
        low = sa
    
    for x in range(high+1):
        if(bd == True):
            gpio.output(bdp, gpio.LOW)
        else :
            gpio.output(bdp, gpio.HIGH)
            
        if(ad == True):
            gpio.output(adpl, gpio.LOW)
            gpio.output(adpnl, gpio.LOW)
        else:
            gpio.output(adpl, gpio.HIGH)
            gpio.output(adpnl, gpio.HIGH)
            
        if(bs > x):
            gpio.output(bsp, gpio.HIGH)
            sleep(.001)
            gpio.output(bsp, gpio.LOW)
            sleep(.001)
            
        if(sa > x):
            gpio.output(aspl, gpio.HIGH)
            gpio.output(aspnl, gpio.HIGH)
            sleep(.001)
            gpio.output(aspl, gpio.LOW)
            gpio.output(aspnl, gpio.LOW)
            sleep(.001)
            

def spinBase(s, d):
    for x in range(s+1):
        if(d == True):
            gpio.output(bdp, gpio.HIGH)
        else:
            gpio.output(bdp, gpio.LOW)
            
        gpio.output(bsp, gpio.HIGH)
        sleep(.001)
        gpio.output(bsp, gpio.LOW)
        sleep(.001)
        
def raiseArm(s, d):
    
    for x in range(s+1):
        if(d == True):
            gpio.output(adpl, gpio.LOW)
            gpio.output(adpnl, gpio.LOW)
        else:
            gpio.output(adpl, gpio.HIGH)
            gpio.output(adpnl, gpio.HIGH)
        
        gpio.output(aspl, gpio.HIGH)
        gpio.output(aspnl, gpio.HIGH)
        sleep(.001)
        gpio.output(aspl, gpio.LOW)
        gpio.output(aspnl, gpio.LOW)
        sleep(.001)
        
        # s = 92 is one spin 
def rotateArm(s, d):
    for x in range(s):
        if(d == True):
            gpio.output(rp, gpio.HIGH)
            sleep(.00175)
            gpio.output(rp, gpio.LOW)
            sleep(.02)
        else:
            gpio.output(rp, gpio.HIGH)
            sleep(.00125)
            gpio.output(rp, gpio.LOW)
            sleep(.02)
    
def rotateEnd(a):
    if(a > 180 or a < 0):
        return; 
    pulseLength = .001 + .00000556*a-.0000004
    for x in range(200):
        gpio.output(ep, gpio.HIGH)
        sleep(pulseLength)
        gpio.output(ep, gpio.LOW)
        sleep(.02)
    
        
        
            
try:
    
    
    
    while True:
        '''
        servo.value = 1
        
        
        sleep(0.5)
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(0.5)
        '''
        
        motion = input("B for base, A for arm base, C for upper joint, Both for base and arm,           A2 for second joint, R to spin arm, E to spin end")
     
        
        if(motion == "B"):
            steps = int(input("Input number of steps (200 = 1 rotation)"))
            value = input("Input direction (Empty = False, any imput = true)")
            boolvalue = bool(value)
            spinBase(steps, boolvalue)
        elif(motion == "A"):
            steps = int(input("Input number of steps (200 = 1 rotation)"))
            value = input("Input direction (Empty = False, any imput = true)")
            boolvalue = bool(value)
            raiseArm(steps, boolvalue)
        elif(motion == "Both"):
            stepsArm = int(input("Steps for arm"))
            armD = input("Direction of arm")
            stepsBase = int(input("Steps for base"))
            baseD = input("Direction of base")
            moveBoth(stepsBase, baseD, stepsArm, armD) 
        elif(motion == "A2"):
            steps = int(input("Input number of steps (200 = 1 rotation)"))
            value = input("Input direction (Empty = False, any imput = true)")
            boolvalue = bool(value)
            armTwo(steps, boolvalue)
        elif(motion == "R"):
            time = int(input("Input number of cycles"))
            value = bool(input("Input direction"))
            rotateArm(time, value)
        elif(motion == "E"):
            angle = int(input("Angle from 0-180"))
            rotateEnd(angle)
            
        
        
        
   
       
    '''
    while True:
        print('Direction CW')
        sleep(.5)
        gpio.output(direction_pin, cw_direction)
        for x in range(400):     # Number of pulses, 200 = one spin
            gpio.output(pulse_pin, gpio.HIGH)
            sleep(.001)           # slows down steps
            gpio.output(pulse_pin, gpio.LOW)
            sleep(.0005)
        print('Direction CCW')
        sleep(.5)
        gpio.output(direction_pin, ccw_direction)
        for x in range(200):
            gpio.output(pulse_pin, gpio.HIGH)
            sleep(.001)
            gpio.output(pulse_pin, gpio.LOW)
            sleep(.00025)   # can be used to alter speed
            
            '''
except KeyboardInterrupt:
    gpio.cleanup()
