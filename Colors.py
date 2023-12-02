from Color import Color
from utils import *

class Colors:

    __instance = None
    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = Colors()
        
        return cls.__instance
    
    def __init__(self):
        self.colorPiece0=Color(0,1)               #Color of the 0 pieces
        self.colorPieceX=Color(0,1)               #Color of the X pieces
        self.colorPiecePlus=Color(0,1)            #Color of the plus pieces
        self.colorPieceMinus=Color(0,1)           #Color of the Minus pieces
        self.colorLineInterception=Color(50,70)   #tabuleiro oficial
        #self.colorLineInterception=Color(70,95)  # casa
        self.colorLine=Color(0,1)                 #Color of the line
        self.colorStatus=Color(0,1)               #Current color status
