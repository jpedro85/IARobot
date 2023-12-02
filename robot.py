#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor,ColorSensor,UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop
from pybricks.tools import wait
from math import pi

from Colors import Colors
from Color import Color
from utils import *
from board import *
from point import *

class Robot:

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = Robot()
        
        return cls.__instance

    def __init__(self):
        self.config()
    
    def config(self):
        # Initialize the EV3 Brick.
        self.ev3 = EV3Brick()
        self.ev3.speaker.set_volume(100)

        # Initialize the motors.
        self.leftMotor = Motor(Port.B)
        self.leftMotor.reset_angle(0)
        self.rightMotor = Motor(Port.C)
        self.rightMotor.reset_angle(0)
        self.grabber= Motor(Port.A)
        self.touch_sensor = TouchSensor(Port.S1)
        self.colorSensor = ColorSensor(Port.S3)
        self.ultrasonicSensor = UltrasonicSensor(Port.S4)
       # self.colors = Colors()
        # Initialize the drive base.
        self.robotDriveBase = DriveBase(self.leftMotor, self.rightMotor, wheel_diameter=25.5, axle_track=145)
        #vars
        self.startPoint = Point(0,0)
        self.minObjectDetectDistance = 40
        self.seePiecesInterval = 1000
        self.adjustForTurn = 30
        self.adjustAfterTurn = -70

    def test(self):
        while True:
            print( self.touch_sensor.pressed())
            if not  self.touch_sensor.pressed():
                self.grabber.run(1000)
            else:
                self.grabber.stop(Stop.HOLD)
                self.grabber.run_until_stalled(-1000,Stop.HOLD)
                break
    
    def testColorReflection(self):
        while True:
           print(self.colorSensor.reflection())

    def testUltrasonicDistance(self):
        while(True):
           print(self.ultrasonicSensor.distance(True))

    def move(self,slots):
        i=0
        enterColor = False
        self.robotDriveBase.drive(100,0)
        while(i<=slots):

            if(Colors.getInstance().colorLineInterception.isColor(self.colorSensor.reflection())):
                enterColor = True

            elif(enterColor):
                print(self.colorSensor.reflection())
                print("At interception: ", i)
                i=i+1
                enterColor = False

        
        self.robotDriveBase.stop()

    def pickPiece(self):
        self.robotDriveBase.straight(110)
        self.grab()
        self.rotate(180)
        self.move(0) #move(0) same as move until Interception
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(-90)
        self.robotDriveBase.straight(self.adjustAfterTurn)

    
    def dropPiece(self):
        self.rotate(45)
        self.robotDriveBase.straight(120)
        self.release()
        self.robotDriveBase.straight(-120)
        self.rotate(125)
        self.robotDriveBase.straight(-130)
       
    def grab(self):
        #Close The Grabber And The Arm Will Rise
        self.grabber.run(1000)
        #Wait Until The Touch Sensor Is Pressed
        while not self.touch_sensor.pressed():    
            pass
        self.grabber.stop()
        print("Grabbing The Piece!")

    def release(self):
        #The motor is working in the opposite direction in order to open the grabber
        self.grabber.run_until_stalled(-450) # Adjusts velocity when needed
        # wait(2000) # Waits 2000 milliseconds (2 seconds) in order to give time to the grabber to open 
        self.grabber.stop(Stop.BRAKE) # Stops the motor
        print("Released Piece!")

    def rotate(self,angle):
        self.robotDriveBase.turn(angle)

    def moveFromStartToPoint(self,point):
        self.move(point.x - self.startPoint.x)
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(90)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.y - self.startPoint.y)

    def moveFromPointToStart(self,point):
        self.move(point.y - self.startPoint.y )
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(-90)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.x - self.startPoint.x)

    def placePiece(self,point):
        self.pickPiece()
        self.moveFromStartToPoint(point)
        self.dropPiece()
        self.moveFromPointToStart(point)
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(90)
        self.robotDriveBase.straight(self.adjustAfterTurn)

    def seePieces(self):

        print("Started reading Pieces!")
        while(True):
            if(Colors.getInstance().colorPiece0.isColor(self.colorSensor.reflection())):
                Board.getInstance().pieces.append(PieceO())

            elif(Colors.getInstance().colorPieceX.isColor(self.colorSensor.reflection())):
                Board.getInstance().pieces.append(PieceX())

            elif(Colors.getInstance().colorPiecePlus.isColor(self.colorSensor.reflection())):
                Board.getInstance().pieces.append(PiecePlus())

            elif(Colors.getInstance().colorPieceMinus.isColor(self.colorSensor.reflection())):
                Board.getInstance().pieces.append(PieceMinus())
                
            elif(Colors.getInstance().colorStatus.isColor(self.colorSensor.reflection())):
                print("Finished reading Pieces!")
                break

            print("Readed:",Board.getInstance().pieces[-1])
            wait(self.seePiecesInterval)