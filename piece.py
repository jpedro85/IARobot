
class Piece:

    def __init__(self,symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol


class PiecePlus(Piece):
    
    def __init__(self):
        super().__init__("+")
        self.shape = ShapePlus.getInstance()



class PieceX(Piece):

    def __init__(self):
        super().__init__("X")
        self.shape = ShapeX.getInstance()




class PieceMinus(Piece):

    def __init__(self):
        super().__init__("-")
        self.shape = ShapeMinus.getInstance()


class PieceO(Piece):
    
    def __init__(self):
        super().__init__("O")
        self.shape = ShapeO.getInstance()


class PieceNone(Piece):
    
    def __init__(self):
        super().__init__(" ")
        self.shape = None


from Shape import *