#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,TouchSensor,ColorSensor,UltrasonicSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase, Stop
from pybricks.tools import wait
from math import pi

from Colors import *
from Color import *
from board import *
from point import *
from piece import *
from sma import SMA,State
from util import Utils
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
        self.ev3.speaker.set_volume(1000)

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
        self.robotDriveBase = DriveBase(self.leftMotor, self.rightMotor, wheel_diameter=25.5, axle_track=140)#25.5 145
        self.robotDriveBase.reset()
        #vars
        self.startPoint = Point(0,0)

    
        self.adjustForTurn = 30
        self.adjustAfterTurn = -70
        self.TURN_RADIUS = 87.5

        #move2
        self.moveV2Margin = 2

        self.board = Board()

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
        self.robotDriveBase.reset()
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
        self.robotDriveBase.straight(180)
        self.grab()
        self.rotate(185)
        self.move(0) #move(0) same as move until Interception
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(-95)
        self.robotDriveBase.straight(self.adjustAfterTurn)

    def dropPiece(self):
        self.rotate(45)
        self.robotDriveBase.straight(120)
        self.release()
        self.robotDriveBase.straight(-110)#120
        self.rotate(133)#125
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
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(90)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.y - self.startPoint.y)

    def moveFromPointToStart(self,point:Point):
        self.move(point.y - self.startPoint.y )
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(-self.TURN_RADIUS)
        self.robotDriveBase.straight(self.adjustAfterTurn)
        self.move(point.x - self.startPoint.x)

    def placePiece(self,point:Point):
        self.pickPiece()
        self.moveFromStartToPoint(point)
        self.dropPiece()
        self.moveFromPointToStart(point)
        self.robotDriveBase.straight(self.adjustForTurn)
        self.rotate(90)
        self.robotDriveBase.straight(self.adjustAfterTurn)

    def readPieces(self,board:Board):

        self.grab()
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

        self.release()

    def playRandom(self):

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
            print(dic)
            if(dic):
                for key in dic.keys():
                    print("Removed:" + key + "count:" + str(dic[key]) )
                    self.ev3.speaker.say("Removed:" + key + "count:" + str(dic[key]) )
        
        print(board)

    def play(self,PercentageOfVariations =0):

        board = self.board

        self.readPieces(board)
        print("Readded Pieces:")
        board.PrintPiecesList()

        wait(2000)
        self.ev3.speaker.say("Starting")
        result= 0
        # playedDic = {'-': {'lst':[] , "l":0},'+':{'lst':[] , "l":0},'O':{'lst':[] , "l":0},'X':{'lst':[] , "l":0} }
        #played = 0
         
        while (len(board.pieces) > 0 ):
            
            print(board)
            chosenSlot = self.choosePlace_1_Neuronio(self.board,PercentageOfVariations)
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
            print(dic)
            if(dic):
                for key in dic.keys():
                    print("Removed:" + key + "count:" + str(dic[key]) )
                    self.ev3.speaker.say("Removed:" + key + "count:" + str(dic[key]) )
                    result += 2**(dic[key])

            # playedDic[piece.symbol]["lst"].append(chosenSlot)
            # playedDic[piece.symbol]["l"] += 1
            # played += 1
        
        left = 2**len(self.board.getAllPieces())
        print(board)
        self.ev3.speaker.say("Result:" + str(result-left))
        print("Result:",result-left)


    def playTest(self,PercentageOfVariations =0):
        result = 0
        print(self.board)
        while( len(self.board.pieces)  >0 ):
            slot = self.choosePlace_1_Neuronio(self.board,PercentageOfVariations)
            piece = self.board.pieces.pop(0)
            slot.piece = piece
            print(slot)
            self.board.slots[slot.point.x][slot.point.y]=slot
            print(self.board)
            d = self.board.clearShapes()
            for key in d.keys():
                print("Removed:" + key + "count:" + str(d[key]) )
                self.ev3.speaker.say("Removed:" + key + "count:" + str(d[key]) )
                result += 2**(d[key])

            print("afterCleared",self.board)
            print("----------------------End Play----------------------")

        left = 2**len(self.board.getAllPieces())
        print(self.board)
        self.ev3.speaker.say("Result:" + str(result-left))
        print("Result:",result-left)

    def choosePlace_1_Neuronio(self,board:Board,PercentageOfVariations = 0):

        def compareNumbers(a,b):
            return -(a-b) if a > b else ( (b-a) if a < b else 0)

        def compareList(list1,list2,numberOfPieces):

            valueInFullShapes = 0
            valueInPossibleShapes = 0
            valueInLostShapes = 0
           # valueInNewForms = 0
            progression = 0

            dict1 = {d['Side']: d for d in list1}
            dict2 = {d['Side']: d for d in list2}

            for side in range(board.size,1,-1):#5--2

                # shapeDic1 = None
                # for dicShape in list1:
                #     if( dicShape["Side"] == side):
                #         shapeDic1 = dicShape

                # shapeDic2 = None
                # for dic_Shape in list2:
                #     if( dic_Shape["Side"] == side):
                #         shapeDic2 = dic_Shape

                shapeDic1 = dict1.get(side)
                shapeDic2 = dict2.get(side)


                if(shapeDic1 != None and shapeDic2 != None):
                # change or not number of pieces in shape

                    if(shapeDic2["Missing"] == 0):
                    #full shape
                        valueInFullShapes += (shapeDic2["ActualNumber"] + shapeDic2["Missing"])
                    elif(shapeDic2["Missing"] <= numberOfPieces-1):
                    #enough pieces for completing 
                        valueInPossibleShapes += (shapeDic2["ActualNumber"] + shapeDic2["Missing"])
                        progression += compareNumbers(shapeDic2["Missing"],shapeDic1["Missing"])

                       
                elif(shapeDic1 != None and shapeDic2 == None): 
                # list2 has less shapes 
                    valueInLostShapes += (shapeDic1["ActualNumber"] + shapeDic1["Missing"])
                    
                elif(shapeDic1 == None and shapeDic2 != None): 
                # list2 has more shapes or different shapes (if different then they are bigger)
                    
                    if(shapeDic2["Missing"] > numberOfPieces-1):
                    #After placing this piece an impossible shape was created or turn into 
                        valueInLostShapes += (shapeDic2["ActualNumber"] + shapeDic2["Missing"])
                    else: 
                        valueInPossibleShapes += (shapeDic2["ActualNumber"] + shapeDic2["Missing"])
                       # progression += 1

                        #valueInNewForms += side
            
                #else None None -> Nothing to compare
                #print("s",side,"d1",shapeDic1,"d2",shapeDic2,"FS:",valueInFullShapes ,"IPS:" , valueInPossibleShapes ,"LS:", valueInLostShapes ,"P:", progression)
                
            
            return valueInFullShapes , valueInPossibleShapes , valueInLostShapes , progression

        def compareDic(dic1,dic2,shapeSymbol,pieceCount):

            #print("compareDic:",shapeSymbol,pieceCount)
            lst1_Of_Dic_WithListOf_Dic = dic1[shapeSymbol]
            lst2_Of_Dic_WithListOf_Dic = dic2[shapeSymbol]
           # print(lst1_Of_Dic_WithListOf_Dic)
            #print(lst2_Of_Dic_WithListOf_Dic)
            i = 0
            l = len(lst1_Of_Dic_WithListOf_Dic)
            valueInFullShapes = 0
            valueInPossibleShapes = 0
            valueInLostShapes = 0
            progression = 0
            while( i < l ):

                valueInFullShapesA , valueInPossibleShapesA , valueInLossShapesA , progressionA = compareList( lst1_Of_Dic_WithListOf_Dic[i]["shapeList"] , lst2_Of_Dic_WithListOf_Dic[i]["shapeList"] , pieceCount[shapeSymbol] )
                
                valueInFullShapes += valueInFullShapesA
                valueInPossibleShapes += valueInPossibleShapesA
                valueInLostShapes +=  valueInLossShapesA
                progression += progressionA

                #print("->",lst1_Of_Dic_WithListOf_Dic[i]["slot"].point,"SY",shapeSymbol,"FS:",valueInFullShapes ,"IPS:" , valueInPossibleShapes ,"LS:", valueInLostShapes ,"P:", progression)
                i += 1

            return valueInFullShapes , valueInPossibleShapes , valueInLostShapes , progression



        if(len(board.pieces) == 0):
            return None
        
        freeSlots = board.getSlotsWithPiecesOfType(PieceNone)
        if(len(freeSlots) == 0):
            return None

        dicPieceCount = board.countPieces()
        print(dicPieceCount)

        dicCountShapesBefore = board.countShapes(1)
        #print(dicCountShapesBefore)
        #printf(dicCountShapesBefore)

        BestValueInFullShapes = None
        BestValueInPossibleShapes = None
        BestValueInLostShapes = None
        BestProgression = None
        BestSlot = None

        for freeSlot in freeSlots:
            #totalChange = 0
            #print("begin:",str(freeSlot))
            board.slots[freeSlot.point.x][freeSlot.point.y].piece = board.pieces[0] #ChangeTheBoard
            #print(board)
            dicCountShapeAfter = board.countShapes(1)
            #print(dicCountShapeAfter)

            valueInFullShapes , valueInPossibleShapes , valueInLostShapes  , progression = compareDic(dicCountShapesBefore,dicCountShapeAfter,"-",dicPieceCount)

            valueInFullShapesA , valueInPossibleShapesA , valueInLostShapesA , progressionA = compareDic(dicCountShapesBefore,dicCountShapeAfter,"+",dicPieceCount)
            valueInFullShapes += valueInFullShapesA
            valueInPossibleShapes += valueInPossibleShapesA
            valueInLostShapes += valueInLostShapesA
            progression += progressionA

            valueInFullShapesA , valueInPossibleShapesA , valueInLostShapesA , progressionA = compareDic(dicCountShapesBefore,dicCountShapeAfter,"X",dicPieceCount)
            valueInFullShapes += valueInFullShapesA
            valueInPossibleShapes += valueInPossibleShapesA
            valueInLostShapes += valueInLostShapesA
            progression += progressionA

            valueInFullShapesA , valueInPossibleShapesA , valueInLostShapesA , progressionA = compareDic(dicCountShapesBefore,dicCountShapeAfter,"O",dicPieceCount)
            valueInFullShapes += valueInFullShapesA
            valueInPossibleShapes += valueInPossibleShapesA
            valueInLostShapes += valueInLostShapesA
            progression += progressionA


            board.slots[freeSlot.point.x][freeSlot.point.y].piece = PieceNone() #reverse change in board
            # 
            # valueInPossibleShapes += valueInPossibleShapesA
            # valueInLostShapes += valueInLossShapesA
            # valueInNewForms += valueInNewFormsA
            # progression += progressionA   
            OPT = -1
            
            print("actual:",freeSlot,":",valueInFullShapes ,"IPS:" , valueInPossibleShapes ,"LS:", valueInLostShapes ,"P:", progression)
            print("A->",OPT,"best:",BestSlot,":",BestValueInFullShapes ,"IPS:" , BestValueInPossibleShapes ,"LS:", BestValueInLostShapes ,"P:", BestProgression)

            if(BestSlot == None):
                BestValueInFullShapes = valueInFullShapes
                BestValueInPossibleShapes = valueInPossibleShapes
                BestValueInLostShapes = valueInLostShapes
                BestProgression = progression
                BestSlot = freeSlot
                OPT =0

            elif(BestValueInFullShapes < valueInFullShapes):
                BestValueInFullShapes = valueInFullShapes
                BestValueInPossibleShapes = valueInPossibleShapes
                BestValueInLostShapes = valueInLostShapes
                BestProgression = progression
                BestSlot = freeSlot
                OPT = 1

            elif(BestValueInFullShapes == valueInFullShapes):
                
                if(BestValueInPossibleShapes < valueInPossibleShapes and BestProgression == progression and BestValueInLostShapes >= valueInLostShapes):    
                    BestValueInFullShapes = valueInFullShapes
                    BestValueInPossibleShapes = valueInPossibleShapes
                    BestValueInLostShapes = valueInLostShapes
                    BestProgression = progression
                    BestSlot = freeSlot
                    OPT = 2

                elif(BestValueInPossibleShapes == valueInPossibleShapes):
                    
                    if(BestProgression < progression):
                            BestValueInFullShapes = valueInFullShapes
                            BestValueInPossibleShapes = valueInPossibleShapes
                            BestValueInLostShapes = valueInLostShapes
                            BestProgression = progression
                            BestSlot = freeSlot
                            OPT = 3

                    elif(BestProgression == progression): #No difference

                        if(BestValueInLostShapes > valueInLostShapes):
                            BestValueInFullShapes = valueInFullShapes
                            BestValueInPossibleShapes = valueInPossibleShapes
                            BestValueInLostShapes = valueInLostShapes
                            BestProgression = progression
                            BestSlot = freeSlot
                            OPT = 4

                        elif(BestValueInLostShapes == valueInLostShapes and random.randint(0,100) < PercentageOfVariations):
                            BestValueInFullShapes = valueInFullShapes
                            BestValueInPossibleShapes = valueInPossibleShapes
                            BestValueInLostShapes = valueInLostShapes
                            BestProgression = progression
                            BestSlot = freeSlot
                            OPT = 5

                elif( BestValueInPossibleShapes < valueInPossibleShapes and  BestProgression < progression):
                    BestValueInFullShapes = valueInFullShapes
                    BestValueInPossibleShapes = valueInPossibleShapes
                    BestValueInLostShapes = valueInLostShapes
                    BestProgression = progression
                    BestSlot = freeSlot
                    OPT = 6

                elif(BestProgression < progression):
                    BestValueInFullShapes = valueInFullShapes
                    BestValueInPossibleShapes = valueInPossibleShapes
                    BestValueInLostShapes = valueInLostShapes
                    BestProgression = progression
                    BestSlot = freeSlot
                    OPT = 7


            print("B->",OPT,"best:",BestSlot,":",BestValueInFullShapes ,"IPS:" , BestValueInPossibleShapes ,"LS:", BestValueInLostShapes ,"P:", BestProgression)

        return BestSlot
    
    def playSimulated(self):

        play:list = self.choosePlace_test()
        result = 0
        playCounter = 0
        while len(self.board.pieces) > 0:
            piece:Piece = self.board.pieces.pop(0)
            placeSlot:Slot = play.pop(0).slot

            self.board.slots[placeSlot.point.x][placeSlot.point.y].piece = piece
            dicRemoveShapes = self.board.clearShapes()
            for key in dicRemoveShapes.keys():
                Utils.print(608,"robot", "Removed " +str(key) + "count:" + str(dicRemoveShapes[key]) + "\n" )
                result += 2**(dicRemoveShapes[key])
            Utils.print(610,"robot","After play " + str(playCounter) + ":" + str(self.board) + "\n\n")

            playCounter+=1

        length = len(self.board.getAllPieces())
        left = (2**length) if length != 0 else 0
        
        Utils.print(612,"robot", "final board:" + str(self.board) + "\n" )
        Utils.print(615,"robot","Final Result:" + str(result - left))

    def choosePlace_test(self):

        path = SMA.start(State(self.board.Copy(),None),10000)
        if(path):
            count = 0
            for state in path:
                print("count:",count,"play:",state.slot)
                count+=1
            return path
        else:
            print("Does't have solution")
            raise LookupError("SMA can not find a solution")