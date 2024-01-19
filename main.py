#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *
from tree import *
import time




robot = Robot.getInstance()

# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PieceMinus())
# robot.board.pieces.append(PieceMinus())

robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceX())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PiecePlus())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceO())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceMinus())
robot.board.pieces.append(PieceO())

start_time = time.time()
robot.playSimulated()
end_time = time.time()

execution_time = end_time - start_time
print("time",execution_time)