#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor,ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop
from pybricks.tools import wait
from math import pi

from Colors import Colors
from Color import Color
from utils import singleton
from board import *

class Robot:

    def __init__(self):
        self.config()
    
    def config(self):
        # Initialize the EV3 Brick.
        self.ev3 = EV3Brick()
        self.ev3.speaker.set_volume(100)

        # Initialize the motors.
        self.leftMotor = Motor(Port.B)
        self.rightMotor = Motor(Port.C)
        self.grabber= Motor(Port.A)
        self.touch_sensor = TouchSensor(Port.S1)
        self.colorSensor = ColorSensor(Port.S3)
        self.colors = Colors()
        # Initialize the drive base.
        self.robotDriveBase = DriveBase(self.leftMotor, self.rightMotor, wheel_diameter=25.5, axle_track=145)

    def test(self):
        while True:
            print( self.touch_sensor.pressed())
            if not  self.touch_sensor.pressed():
                self.grabber.run(1000)
            else:
                self.grabber.stop(Stop.HOLD)
                self.grabber.run_until_stalled(-1000,Stop.HOLD)
                break
    
    def test2(self):
        while True:
           print(self.colorSensor.reflection())

    def move(self,quadriculas):
        i=0
        self.robotDriveBase.drive(100,0)
        while(i<quadriculas):
            if(self.colors.colorLineInterception.isColor(self.colorSensor.reflection())):
                i=i+1
            wait(120)
        
        self.robotDriveBase.stop()
       
    def grab(self):
        print("Grabbing The Object!")
        #Close The Grabber And The Arm Will Rise
        self.grabber.run(1000)
        #Wait Until The Touch Sensor Is Pressed
        while not self.touch_sensor.pressed():    
            pass
        # This Loop Waits For The Touch Sensor To Be Pressed
        self.grabber.stop()

    def release(self):
        #The motor is working in the opposite direction in order to open the grabber
        print("Releasing Object!")
        self.grabber.run_until_stalled(-500) # Adjusts velocity when needed
        # wait(2000) # Waits 2000 milliseconds (2 seconds) in order to give time to the grabber to open 
        self.grabber.stop(Stop.BRAKE) # Stops the motor

    def rotate(self,angle):
        self.robotDriveBase.turn(angle)


# leftMotor = Motor(Port.B)
# rightMotor = Motor(Port.C)
# grabber= Motor(Port.A)
# touch_sensor = TouchSensor(Port.S1)

# WHEEL_DIAMETER=25.5
# AXLE_TRACK=145


# robotDriveBase = DriveBase(leftMotor, rightMotor, WHEEL_DIAMETER,AXLE_TRACK)