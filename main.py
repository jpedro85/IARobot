#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *
from tree import *

f = Tree()
f.addValue(0)
f.addValue(-6)
f.addValue(8)
f.addValue(-2)
f.addValue(6)
f.addValue(-1)
f.addValue(-3)
f.addValue(-10)
f.addValue(7)
f.addValue(8)

f.printOrder()
print("------------------------")
f.print_tree()
print(f.popLowestValue())
print("------------------------")
f.print_tree()
print(f.popLowestValue())
print("------------------------")
f.print_tree()


print(f.getNodeWithHigherValue())
print(f.getNodeWithLowestValue())

f.printOrder()
print(f.getValueByIndex(7))

# robot = Robot.getInstance()

# # robot.board.pieces.append(PieceMinus())
# # robot.board.pieces.append(PieceMinus())
# # robot.board.pieces.append(PieceMinus())

# robot.board.pieces.append(PiecePlus())
# robot.board.pieces.append(PiecePlus())



# #robot.playTest()
# robot.choosePlace_test()