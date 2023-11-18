#!/usr/bin/env pybricks-micropython
# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor)
# from pybricks.parameters import Port, Stop, Direction, Button, Color
# from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop

import Colors
import Color

@singleton

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
        # Initialize the drive base.
        self.robotDriveBase = DriveBase(leftMotor, rightMotor, wheel_diameter=25.5, axle_track=145)

    def move(self,quadriculas):
        i=0
        self.robotDriveBase.straight(slotDistance*5+10)
        while(i<quadriculas):
            if(Colors.colorLineIntercection.isColor()):
                i=i+1
        self.robotDriveBase.stop()
