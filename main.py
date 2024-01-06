#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *

robot = Robot.getInstance()

# robot.board.slots[3][1]=Slot(3,1,PieceMinus())
# robot.board.slots[1][1]=Slot(1,1,PiecePlus())
# robot.board.slots[1][2]=Slot(0,4,PiecePlus())
# robot.board.slots[2][1]=Slot(2,1,PieceX())
# robot.board.slots[2][3]=Slot(2,3,PieceX())
# robot.board.slots[4][3]=Slot(4,3,PieceO())
# robot.board.slots[4][4]=Slot(4,4,PieceO())

#robot.play()
#robot.testColorRGB()

# robot.rotate(90)
# robot.rotate(-45)
# robot.rotate(180)
# robot.rotate(45)
# robot.rotate(90)
# robot.rotate(-360)

print(robot.board)
#robot.placePiece(Point(3,3))
#robot.readPieces(robot.board)
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PiecePlus())


# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PiecePlus())
# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PieceO())
# robot.board.pieces.append(PieceO())
# robot.board.pieces.append(PieceX())
# robot.board.pieces.append(PiecePlus())
# robot.board.pieces.append(PieceO())
# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PieceO())
# robot.board.pieces.append(PiecePlus())
# robot.board.pieces.append(PiecePlus())
# robot.board.pieces.append(PiecePlus())

robot.playTest()