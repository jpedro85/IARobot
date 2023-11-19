#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop
from pybricks.tools import wait
from math import pi

# Initialize the EV3 Brick.
ev3 = EV3Brick()
ev3.speaker.set_volume(100)

# Initialize the motors.
leftMotor = Motor(Port.B)
rightMotor = Motor(Port.C)
grabber= Motor(Port.A)
touch_sensor = TouchSensor(Port.S1)

WHEEL_DIAMETER=25.5
AXLE_TRACK=145


robotDriveBase = DriveBase(leftMotor, rightMotor, WHEEL_DIAMETER,AXLE_TRACK)


def grab():
    print("Grabbing The Object!")
    #Close The Grabber And The Arm Will Rise
    grabber.run(1000)
    #Wait Until The Touch Sensor Is Pressed
    while not touch_sensor.pressed():    
        pass
    # This Loop Waits For The Touch Sensor To Be Pressed
    grabber.stop()

def release():
    #The motor is working in the opposite direction in order to open the grabber
    print("Releasing Object!")
    grabber.run(-1000) # Adjusts velocity when needed
    wait(2000) # Waits 2000 milliseconds (2 seconds) in order to give time to the grabber to open 
    grabber.stop(Stop.BRAKE) # Stops the motor

def rotate(angle):
    # Converta o ângulo para milímetros usando o diâmetro da roda e pi.
    # Uma revolução é 2 * pi * diâmetro da roda milímetros.
    millimeters = (angle / 360) * 2 * pi * WHEEL_DIAMETER

    # Calcule a velocidade do motor para alcançar a rotação desejada.
    # Ajuste esta fórmula para controlar a velocidade e a rotação do seu robô.
    speed = (millimeters / 1000) * 100

    # Roda o robô usando a base de acionamento.
    robotDriveBase.drive(0, speed)
