#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *

robot = Robot.getInstance()

# robot.board.slots[0][1]=Slot(0,1,PieceMinus())
# robot.board.slots[2][1]=Slot(2,1,PiecePlus())
# robot.board.slots[2][3]=Slot(2,3,PieceMinus())
# robot.board.slots[0][4]=Slot(0,4,PiecePlus())
# robot.board.slots[1][1]=Slot(1,1,PieceMinus())
# robot.board.slots[3][4]=Slot(3,4,PiecePlus())
# #robot.board.slots[4][1]=Slot(4,1,PieceMinus())
# robot.board.slots[3][0]=Slot(3,0,PiecePlus())
# robot.board.slots[2][0]=Slot(2,0,PieceMinus())
# robot.board.slots[1][4]=Slot(1,4,PiecePlus())
# robot.board.slots[0][3]=Slot(0,3,PieceMinus())
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
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())

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

print(robot.board)
while( len(robot.board.pieces)  >0 ):
    slot = robot.choosePlace(robot.board)
    piece = robot.board.pieces.pop(0)
    slot.piece = piece
    print(slot)
    robot.board.slots[slot.point.x][slot.point.y]=slot
    print(robot.board)
    robot.board.clearShapes()
    print("afterCleared",robot.board)
    print("----------------------End Play----------------------")