#!/usr/bin/env pybricks-micropython
from robot import Robot
from point import *

robot = Robot.getInstance()

#robot.testColorReflection()
#robot.release()
#robot.testUltrasonicDistance()
robot.placePiece(Point(1,3))
#robot.moveFromStartToPoint(Point(2,2))