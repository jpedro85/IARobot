
class Piece:

    def __init__(self,symbol,shape):
        self.symbol = symbol
        self.shape = shape

    def __str__(self):
        return self.symbol

class PiecePlus(Piece):

    def __init__(self):
        super().__init__("+",ShapePlus.getInstance())


class PieceX(Piece):

    def __init__(self):
        super().__init__("X",ShapeX.getInstance())


class PieceMinus(Piece):

    def __init__(self):
        super().__init__("-",ShapeMinus.getInstance())


class PieceO(Piece):
    
    def __init__(self):
        super().__init__("O",ShapeO.getInstance())


class PieceNone(Piece):
    
    def __init__(self):
        super().__init__(" ",None)


from Shape import *