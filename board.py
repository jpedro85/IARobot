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
    
    def __init__(self,size=5):
        self.size = size
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
    
    def getAllPieces(self):
        pieces = []
        for x in range(self.size):
            for y in range(self.size):
                if type(self.slots[x][y].piece) != PieceNone:
                    pieces.append(self.slots[x][y])

        return pieces

    def Copy(self):
        newBoard = Board()

        # Dictionary mapping piece types to their constructors
        piece_type_to_constructor = {
            PieceMinus: PieceMinus,
            PieceX: PieceX,
            PieceO: PieceO,
            PiecePlus: PiecePlus,
            PieceNone: PieceNone
        }

        for x in range(self.size):
            for y in range(self.size):
                piece_type = type(self.slots[x][y].piece)
                # Use the dictionary to create a new piece or reuse the same piece if they are immutable
                newBoard.slots[x][y].piece = piece_type_to_constructor.get(piece_type, PieceNone)()

        # Copying pieces list using list comprehension
        newBoard.pieces = [piece_type_to_constructor.get(type(p), PieceNone)() for p in self.pieces]

        return newBoard

    def clearShapes(self):
        """
        return { type(piece).__name__ : count , ... }
        """
        count_dict = {}
        for x in range(5):
            for y in range(5):
                piece = self.slots[x][y].piece
                # Skip if the slot is empty or has a PieceNone
                if piece is None or isinstance(piece, PieceNone):
                    continue
                
                piece_type = type(piece).__name__
                count = piece.shape.clearCompletedShapeBasedOnPoint(self.slots[x][y], self)

                # Aggregate count for each piece type
                if count > 0:
                    count_dict[piece_type] = count_dict.get(piece_type, 0) + count

        return count_dict

    def countPieces(self):
        """
        :return: a dictionary `dic` which contains the count of each symbol in the `self.pieces` list.
        The keys of the dictionary are "-", "X", "O", and "+", and the values are the count of each
        symbol in the list.
        """
        dic = { "-" : 0 , "X" : 0 , "O" : 0 , "+" : 0 }
        for piece in self.pieces:
            dic[piece.symbol] += 1

        return dic
    
    def countShapes(self, minPieces: int = 2):
        """
        return: {"+":
                    [ 
                        { "slot" : slot , 
                            "shapeList" : [ 
                                { "Side" : int, "ActualNumber" : int, "Missing" : int}
                            ] },
                    ] }
        """

        # Reuse shape instances
        shape_plus = ShapePlus.getInstance()
        shape_x = ShapeX.getInstance()
        shape_o = ShapeO.getInstance()
        shape_minus = ShapeMinus.getInstance()

        dic = {"-": [], "X": [], "O": [], "+": []}
        for x in range(5):
            for y in range(5):
                slot = self.slots[x][y]
                slot_str = str(slot)  # Convert to string once per slot

                dic["+"].append({
                    "slot": slot,
                    "str": slot_str,
                    "shapeList": shape_plus.getAllIncompleteShapeBasedOnPoint(self, slot, minPieces=minPieces)
                })

                dic["X"].append({
                    "slot": slot,
                    "str": slot_str,
                    "shapeList": shape_x.getAllIncompleteShapeBasedOnPoint(self, slot, minPieces=minPieces)
                })

                dic["O"].append({
                    "slot": slot,
                    "str": slot_str,
                    "shapeList": shape_o.getAllIncompleteShapeBasedOnPoint(self, slot, minPieces=minPieces)
                })

                dic["-"].append({
                    "slot": slot,
                    "str": slot_str,
                    "shapeList": shape_minus.getAllIncompleteShapeBasedOnPoint(self, slot, minPieces=minPieces)
                })

        return dic


    def getBestShapeForEachShape(self,totalPieces):
        """
        returns: { "-" : {"side":v, "points":v, "left":v ,"count":v , "total":v }} , ... }
        left is the number of pieces that are left outside
        """         
        dicReturn = { 
                "-" : {"side":0, "points":0, "left":0 ,"count":0 , "total":0 } , 
                "X" : {"side":0, "points":0, "left":0 ,"count":0 , "total":0 } , 
                "O" : {"side":0, "points":0, "left":0 ,"count":0 , "total":0 } ,
                "+" : {"side":0, "points":0, "left":0 ,"count":0 , "total":0 } 
                }
        
        #focar mais para o meio ?
        
        for x in range(self.size):
            for y in range(self.size):
                slot = self.slots[x][y]

                dic = ShapeMinus.getInstance().getBestPossibleShapeBasedOnPoint(self,slot,totalPieces["-"])
                if(
                   (dic.get("points") > dicReturn.get("-").get("points")) or 
                   (dic.get("points") == dicReturn.get("-").get("points") and dic.get("piecesLeft") < dicReturn.get("-").get("left"))
                  ):
                    dicReturn.get("-")["side"] = dic.get("side")
                    dicReturn.get("-")["points"] = dic.get("points")
                    dicReturn.get("-")["left"] = dic.get("piecesLeft")
                    dicReturn.get("-")["count"] = dic.get("count")
                    dicReturn.get("-")["total"] = dic.get("total")

                dic:dict = ShapePlus.getInstance().getBestPossibleShapeBasedOnPoint(self,slot,totalPieces["+"]) 
                if(
                   (dic.get("points") > dicReturn.get("+").get("points")) or 
                   (dic.get("points") == dicReturn.get("+").get("points") and dic.get("piecesLeft") < dicReturn.get("+").get("left"))
                  ):
                    dicReturn.get("+")["side"] = dic.get("side")
                    dicReturn.get("+")["points"] = dic.get("points")
                    dicReturn.get("+")["left"] = dic.get("piecesLeft")
                    dicReturn.get("+")["count"] = dic.get("count")
                    dicReturn.get("+")["total"] = dic.get("total")
                

                dic = ShapeX.getInstance().getBestPossibleShapeBasedOnPoint(self,slot,totalPieces["X"])
                if(
                   (dic.get("points") > dicReturn.get("X").get("points")) or 
                   (dic.get("points") == dicReturn.get("X").get("points") and dic.get("piecesLeft") < dicReturn.get("X").get("left"))
                  ):
                    dicReturn.get("X")["side"] = dic.get("side")
                    dicReturn.get("X")["points"] = dic.get("points")
                    dicReturn.get("X")["left"] = dic.get("piecesLeft")
                    dicReturn.get("X")["count"] = dic.get("count")
                    dicReturn.get("X")["total"] = dic.get("total")

                dic = ShapeO.getInstance().getBestPossibleShapeBasedOnPoint(self,slot,totalPieces["O"])
                if(
                   (dic.get("points") > dicReturn.get("O").get("points")) or 
                   (dic.get("points") == dicReturn.get("O").get("points") and dic.get("piecesLeft") < dicReturn.get("O").get("left"))
                  ):
                    dicReturn.get("O")["side"] = dic.get("side")
                    dicReturn.get("O")["points"] = dic.get("points")
                    dicReturn.get("O")["left"] = dic.get("piecesLeft")
                    dicReturn.get("O")["count"] = dic.get("count")
                    dicReturn.get("O")["total"] = dic.get("total")

        return dicReturn


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
