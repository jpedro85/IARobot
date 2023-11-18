#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop

# Initialize the EV3 Brick.
ev3 = EV3Brick()
ev3.speaker.set_volume(100)

# Initialize the motors.
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabber= Motor(Port.A)
touch_sensor = TouchSensor(Port.S1)
