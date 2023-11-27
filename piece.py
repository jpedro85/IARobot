class Piece:

    def __init__(self,symbol):
        self.symbol

    def __str__(self):
        return "symbol: {self.symbol}"

    


class PiecePlus(Piece):
    
    def __init__(self):
        super("+")


class PieceMinus(Piece):

    def __init__(self):
        super("-")

class PieceX(Piece):
    
    def __init__(self):
        super("X")

class PieceO(Piece):
    
    def __init__(self):
        super("O")

class PieceNone(Piece):
    
    def __init__(self):
        super("")

