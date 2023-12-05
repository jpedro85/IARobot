#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board
from point import *

robot = Robot.getInstance()

#robot.release()
robot.testColorRGB()
#robot.testUltrasonicDistance()
#robot.placePiece(Point(2,2))
#robot.grab()
robot.move(3)
print(robot.testTuplo)
#b = Board.getInstance()
#print(b)
#b.clearShapes()
#print(b)

#robot.moveFromStartToPoint(Point(2,2))2255