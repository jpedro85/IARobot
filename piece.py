
class Piece:

    def __init__(self,symbol,shape):
        self.symbol = symbol
        self.shape = shape

    def __str__(self):
        return self.symbol

class PiecePlus(Piece):

    def __init__(self):
        super().__init__("+",ShapePlus.getInstance())

    def __str__(self):
        return self.symbol


class PieceX(Piece):

    def __init__(self):
        super().__init__("X",ShapeX.getInstance())

    def __str__(self):
        return self.symbol

class PieceMinus(Piece):

    def __init__(self):
        super().__init__("-",ShapeMinus.getInstance())
    
    def __str__(self):
        return self.symbol


class PieceO(Piece):
    
    def __init__(self):
        super().__init__("O",ShapeO.getInstance())

    def __str__(self):
        return self.symbol

class PieceNone(Piece):
    
    def __init__(self):
        super().__init__(" ",None)

    def __str__(self):
        return self.symbol


from Shape import *