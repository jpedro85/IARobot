from point import *

class Board:

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = Robot()
        
        return cls.__instance

    def __init__(self):
        
        self.pieces = []
        self.slots = []
        y = -1
        for i in range(25):
            if(i%5 == 0):
                y += 1
            slots.append(Slot(i%5,y))

    def __str__(self):

        line = ""
        for i in range(25):
            if(i%5 == 0):
                print(line)
                line = ""
            line += slots[i]

    class Slot:

        def __init__(self,x,y,piece = None):
            self.point = Point(x,y)
            if(piece == None):
                self.piece = PieceNone()
            else:
                self.piece = piece 

        def __str__(self):
            return "X: {self.point}, Y: {self.piece}"

        
