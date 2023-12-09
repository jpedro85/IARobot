#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *
from Shape import *

robot = Robot.getInstance()

# robot.release()
#robot.testColorRGB()
#robot.testUltrasonicDistance()
#robot.pickPiece()
# robot.placePiece(Point(2,2))
#robot.placePiece(Point(3,2))
#robot.placePiece(Point(1,4))
#robot.grab()
#robot.move(1)
#print(robot.testTuplo)
b = Board.getInstance()

b.slots[0][0]=Slot(0,0,PieceMinus())
b.slots[0][1]=Slot(0,1,PieceMinus())
b.slots[0][2]=Slot(0,2,PiecePlus())
b.slots[1][2]=Slot(1,2,PiecePlus())
b.slots[2][2]=Slot(2,2,PiecePlus())
b.slots[3][2]=Slot(3,2,PiecePlus())
b.slots[4][2]=Slot(4,2,PiecePlus())
b.slots[2][0]=Slot(2,0,PiecePlus())
b.slots[2][1]=Slot(2,1,PiecePlus())
b.slots[2][2]=Slot(2,2,PiecePlus())
b.slots[2][3]=Slot(2,3,PiecePlus())
b.slots[2][4]=Slot(2,4,PiecePlus())

print(b)
b.clearShapes()
print(b)

#robot.moveFromStartToPoint(Point(2,2))22555555555555555555