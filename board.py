from point import *
from piece import *
from Shape import ShapePlus,ShapeMinus,ShapeO,ShapeX
import random


class Slot:
    def __init__(self, x, y, piece=None):
        self.point = Point(x, y)
        if piece == None:
            self.piece = PieceNone()
        else:
            self.piece = piece

    def __str__(self):
        return "( {0} P{1} )".format(str(self.point), str(self.piece))


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
                sl = Slot(i, y)
                sl.piece = PieceNone()
                self.slots[i].append(sl)

                # r = random.randint(0, 3)
                # if r == 0:
                #     s.piece = PieceMinus()
                # elif r == 1:
                #     s.piece = PiecePlus()
                # elif r == 2:
                #     s.piece = PieceO()
                # elif r == 3:
                #     s.piece =PieceX()
                #self.slots[i].append(s)

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

        arrayRemoved_dic = {}
        for x in range(5):
            for y in range(5):
                slot = self.slots[x][y]
                piece = slot.piece
                if piece != None and type(piece) != PieceNone:
                    # if(type(piece) == PiecePlus):
                    count = piece.shape.clearCompletedShapeBasedOnPoint(slot, self)
                    
                    if(count > 0): 
                        arrayRemoved_dic.update( { type(piece).__name__ : count } )

        return arrayRemoved_dic
    
    def countPieces(self):
        """
        :return: a dictionary `dic` which contains the count of each symbol in the `self.pieces` list.
        The keys of the dictionary are "-", "X", "O", and "+", and the values are the count of each
        symbol in the list.
        """
        dic = { "-" : 0 , "X" : 0 , "O" : 0 , "+" : 0 }
        for piece in self.pieces:
            dic[piece.symbol] = dic[ piece .symbol] + 1

        return dic
    
    def countShapes(self,minPieces:int = 2):
        """
        return: {"+":
                    [ 
                        { "slot" : slot , 
                            "shapeList" : [ 
                                { "Side" : int, "ActualNumber" : int, "Missing" : int}
                            ] },
                    ] }
        """
        
        dic = { "-" : [] , "X" : [] , "O" : [] , "+" : [] }
        for x in range(5):
            for y in range(5):
                slot = self.slots[x][y]

                dic["+"].append( 
                    { "slot" : slot , "str" : str(slot),
                    "shapeList" : ShapePlus.getInstance().getAllIncompleteShapeBasedOnPoint(self,slot,minPieces=minPieces) 
                    } )
                
                dic["X"].append( 
                    { "slot" : slot , "str" : str(slot),
                    "shapeList" : ShapeX.getInstance().getAllIncompleteShapeBasedOnPoint(self,slot,minPieces=minPieces) 
                    } )
                
                dic["O"].append( 
                    { "slot" : slot , "str" : str(slot),
                    "shapeList" : ShapeO.getInstance().getAllIncompleteShapeBasedOnPoint(self,slot,minPieces=minPieces) 
                    } )
                
                dic["-"].append( 
                    { "slot" : slot , "str" : str(slot),
                    "shapeList" : ShapeMinus.getInstance().getAllIncompleteShapeBasedOnPoint(self,slot,minPieces=minPieces) 
                    } )

        return dic


    def PrintPiecesList(self):
        for piece in self.pieces:
            print(piece)

    def __str__(self):
        line = ""
        for i in range(5):
            line += "\n"
            for y in range(5):
                line += str(self.slots[i][y]) + ";"

        return line
