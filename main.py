#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board
from point import *

robot = Robot.getInstance()

#robot.testColorReflection()
#robot.release()
#robot.testUltrasonicDistance()
#robot.placePiece(Point(1,3))

b = Board.getInstance()
print(b)
b.clearShapes()
print(b)

#robot.moveFromStartToPoint(Point(2,2))