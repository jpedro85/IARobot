#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor,ColorSensor,UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop
from pybricks.tools import wait
from math import pi

from Colors import *
from Color import *
from utils import *
from board import *
from point import *
import random

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
        self.colorsRGB = ColorsRGB.getInstance()
        # Initialize the drive base.
        self.robotDriveBase = DriveBase(self.leftMotor, self.rightMotor, wheel_diameter=25.5, axle_track=145)
        self.robotDriveBase.reset()
        #vars
        self.startPoint = Point(0,0)
        self.minObjectDetectDistance = 40
        self.seePiecesInterval = 1000
        self.adjustForTurn = 50
        self.adjustAfterTurn = -70
        self.TURN_RADIUS = 87.5
        #move2
        self.moveV2Margin = 2

        self.board = Board.getInstance()

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

    def testColorRGB(self):
        while True:
            rgbColor = self.colorSensor.rgb()
            print(rgbColor)
            # if(ColorsRGB.getInstance().colorLineInterception.isColorRgb(rgbColor)):
            # self.ev3.speaker.beep()


    def testUltrasonicDistance(self):
        while(True):
            print(self.ultrasonicSensor.distance(True))

    def move(self,slots):
        i=0
        enterColor = False
        self.robotDriveBase.drive(100,0)
        while(i<=slots):

            rgbColor = self.colorSensor.rgb()
            result = self.colorsRGB.colorLineInterception.isColorRgb(rgbColor)
            if(result):
                enterColor = True

            elif(enterColor):
                self.ev3.speaker.beep()
                print("At interception: ", i)
                i=i+1
                enterColor = False
            else:
                pass

        self.robotDriveBase.stop()

    # def moveV2(self,slots):
    #     i=0
    #     enterColor = False
    #     self.robotDriveBase.drive(100,0)

    #     while(i<=slots):

    #         rgbColor = self.colorSensor.rgb()
    #         isInterception = self.colorsRGB.colorLineInterception.isColorRgb(rgbColor)
    #         isInLine = self.colorsRGB.colorLine.isColorRgb(rgbColor)

    #         if(not isInLine and not isInterception):
    #             Distance, driveSpeed, Angle, turnRate = self.robotDriveBase.state()
    #             print(self.robotDriveBase.state())
    #             if(turnRate < 0 + self.moveV2Margin):
    #                 self.robotDriveBase.drive(100,-turnRate*3)
                    
    #             elif(turnRate > 0 - self.moveV2Margin):
    #                 self.robotDriveBase.drive(100,turnRate*3)
                    
    #         if(isInterception):
    #             enterColor = True
    #         elif(enterColor):
    #             self.ev3.speaker.beep()
    #             print("At interception: ", i)
    #             i=i+1
    #             enterColor = False
        
    #     self.robotDriveBase.stop()
    #     self.robotDriveBase.reset()

    def pickPiece(self):
        self.robotDriveBase.straight(200)
        self.grab()
        self.rotate(187)
        self.move(0) #move(0) same as move until Interception
        self.robotDriveBase.straight(13)
        self.rotate(-93)
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
        self.robotDriveBase.reset()
        self.robotDriveBase.turn(angle)

    def moveFromStartToPoint(self,point:Point):
        self.move(point.x - self.startPoint.x)
        self.robotDriveBase.straight(self.adjustForTurn-10)
        self.rotate(self.TURN_RADIUS)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.y - self.startPoint.y)

    def moveFromPointToStart(self,point:Point):
        self.move(point.y - self.startPoint.y )
        self.robotDriveBase.straight(self.adjustForTurn-20)
        self.rotate(-self.TURN_RADIUS)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.x - self.startPoint.x)

    def placePiece(self,point:Point):
        self.pickPiece()
        self.moveFromStartToPoint(point)
        self.dropPiece()
        self.moveFromPointToStart(point)
        self.robotDriveBase.straight(self.adjustForTurn-15)
        self.rotate(self.TURN_RADIUS)
        self.robotDriveBase.straight(self.adjustAfterTurn)

    def readPieces(self,board:Board):

        print("Started reading Pieces!")
        lastSymbol = ' '
        
        while(True):
            
            currentColor = self.colorSensor.rgb()
            if(self.colorsRGB.colorPiece0.isColorRgb(currentColor)):
                # Check if the the color was the same that was last read
                # if it was it pauses the program to not spam the symbol to the board pieces sequence
                if (lastSymbol == 'O'):
                    wait(500)
                    
                self.ev3.speaker.say("O")
                board.addPiece("O")
                lastSymbol = "O"

            elif(self.colorsRGB.colorPieceX.isColorRgb(currentColor)):
                # Check if the the color was the same that was last read
                # if it was it pauses the program to not spam the symbol to the board pieces sequence
                if (lastSymbol == 'X'):
                    wait(500)
                
                self.ev3.speaker.say("X")
                board.addPiece("X")
                lastSymbol = "X"

            elif(self.colorsRGB.colorPiecePlus.isColorRgb(currentColor)):
                # Check if the the color was the same that was last read
                # if it was it pauses the program to not spam the symbol to the board pieces sequence
                if (lastSymbol == '+'):
                    wait(500)

                self.ev3.speaker.say("Plus")
                board.addPiece("+")
                lastSymbol = "+"

            elif(self.colorsRGB.colorPieceMinus.isColorRgb(currentColor)):
                # Check if the the color was the same that was last read
                # if it was it pauses the program to not spam the symbol to the board pieces sequence
                if (lastSymbol == '-'):
                    wait(500)

                self.ev3.speaker.say("Minus")
                board.addPiece("-")
                lastSymbol = "-"
                    
            # If the color is equal to the Status color the robot stops reading colors and starts putting the pieces
            elif(self.colorsRGB.colorStatus.isColorRgb(currentColor) ):
                self.ev3.speaker.beep()
                print("Finished Reading Pieces")
                break

    def play(self):

        board = self.board #Board.getInstance()

        self.readPieces(board)
        print("Readded Pieces:")
        board.PrintPiecesList()

        wait(2000)
        self.ev3.speaker.say("Starting")
        
        while (len(board.pieces) > 0 ):
            
            print(board)
            #choose freeSlot
            freeSlots = board.getSlotsWithPiecesOfType(PieceNone)
            chosenSlot = freeSlots[random.randint(0,len(freeSlots)-1)]
            #addPiece and remove from List
            piece = board.pieces.pop(0)

            print("Waiting for next piece:" , str(piece) )
            self.ev3.speaker.say("Waiting for next piece" + str(piece) )
            wait(1)
            chosenSlot.piece = piece
            self.ev3.speaker.say("next Point" + str(chosenSlot.point))
            print("chosenSlot:",str(chosenSlot.point))
            #place
            self.placePiece(chosenSlot.point)

            dic = board.clearShapes()
            for key in dic.keys():
                print("Removed:" + key + "count:" + dic[key] )
                self.ev3.speaker.say("Removed:" + key + "count:" + dic[key])
        
        print(board)

            

        

