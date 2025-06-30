import ikpy.chain
import ikpy.utils.plot as plot_utils

import numpy as np
import time
import math

import ipywidgets as widgets
import serial

from time import sleep


my_chain = ikpy.chain.Chain.from_urdf_file("armfour.urdf",active_links_mask=[False, True, True, True, True, True])

target_position = [ 0, -.3,0]

target_orientation = [0, 0, 1]

ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Y")
print("The angles of each joints are : ", list(map(lambda r:math.degrees(r),ik.tolist())))
# converted to degrees 
baseangle = math.degrees(ik[1])
armoneangle = math.degrees(ik[2])
armtwoangle = math.degrees(ik[3])
spin = math.degrees(ik[4])
armthreeangle = math.degrees(ik[5])
#print(baseangle, armoneangle)

computed_position = my_chain.forward_kinematics(ik)
print("Computed position: %s, original position : %s" % (computed_position[:3, 3], target_position))
print("Computed position (readable) : %s" % [ '%.2f' % elem for elem in computed_position[:3, 3] ])



import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')
my_chain.plot(my_chain.inverse_kinematics(target_position), ax)
matplotlib.pyplot.show()

def doIK():
    global ik
    old_position= ik.copy()
    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)

def updatePlot():
    ax.clear
    my_chain.plot(my_chain.inverse_kinematics(target_position), ax)
    matplotlib.pyplot.show()
    
def move(x,y,z):
    global target_position
    target_position = [x,y,z]
    doIK()
    updatePlot()

   # sendCommand(ik[1].item(),ik[2].item(),ik[3].item(),ik[4].item(),ik[5].item(),ik[6].item(),1)
    
#move(0,0.2,0.3)
#print("The angles of each joints are : ", list(map(lambda r:math.degrees(r),ik.tolist())))
#sleep(5)
#move(.2,.2,.2)
