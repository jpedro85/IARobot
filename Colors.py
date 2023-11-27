from Color import Color
from utils import singleton

class Colors:
    
    def __init__(self):
        self.colorPiece0=Color(0,1)               #Color of the 0 pieces
        self.colorPieceX=Color(0,1)               #Color of the X pieces
        self.colorPiecePlus=Color(0,1)            #Color of the plus pieces
        self.colorPieceMinus=Color(0,1)           #Color of the Minus pieces
        #self.colorLineInterception=Color(7,10)     #Color of the Line intercection
        self.colorLineInterception=Color(47,59)  
        self.colorLine=Color(0,1)                 #Color of the line
        self.colorStatus=Color(0,1)               #Current color status
