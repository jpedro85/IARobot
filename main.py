#!/usr/bin/env pybricks-micropython
from robot import Robot
from board import Board,Slot
from point import *
from piece import *
from tree import *





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

robot.playSimulated()