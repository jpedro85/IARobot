from point import *
from piece import *
import random


class Slot:
    def __init__(self, x, y, piece=None):
        self.point = Point(x, y)
        if piece == None:
            self.piece = PieceNone()
        else:
            self.piece = piece

    def __str__(self):
        return " ( {0} P:{1} )".format(str(self.point), str(self.piece))


class Board:
    __instance = None

    @classmethod
    def getInstance(cls):
        if cls.__instance == None:
            cls.__instance = Board()

        return cls.__instance

    def __init__(self):
        self.size = 5
        self.pieces = []
        self.slots = []
        for i in range(5):
            self.slots.append([])

            for y in range(5):
                s = Slot(i, y)
                r = random.randint(0, 3)

                if r == 0:
                    s.piece = PieceMinus()
                elif r == 1:
                    s.piece = PiecePlus()
                elif r == 2:
                    s.piece = PieceO()
                elif r == 3:
                    s.piece =PieceX()

                self.slots[i].append(s)

    def addPiece(self, pieceSymbol):
        print("Board.py line 51: Added Piece", pieceSymbol)
        if "-" == pieceSymbol:
            self.pieces.append(PieceMinus())
        elif "X" == pieceSymbol:
            self.pieces.append(PieceX())
        elif "O" == pieceSymbol:
            self.pieces.append(PieceO())
        elif "+" == pieceSymbol:
            self.pieces.append(PiecePlus())
        else:
            print("Add Piece Invalid Piece")

    def getSlotsWithPiecesOfType(self, piceType):
        pieces = []
        for x in range(self.size):
            for y in range(self.size):
                if type(self.slots[x][y].piece) == piceType:
                    pieces.append(self.slots[x][y])

        return pieces

    def clearShapes(self):
        for x in range(5):
            for y in range(5):
                slot = self.slots[x][y]
                piece = slot.piece
                if piece != None and type(piece) != PieceNone:
                    # if(type(piece) == PiecePlus):
                    piece.shape.clearCompletedShapeBasedOnPoint(slot, self)

    def __str__(self):
        line = ""
        for i in range(5):
            line += "\n"
            for y in range(5):
                line += str(self.slots[i][y]) + ";"

        return line
