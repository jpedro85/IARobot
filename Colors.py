from Color import *
from utils import *

class ColorsReflection:

    __instance = None
    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = Colors()
        
        return cls.__instance
    
    def __init__(self):
        self.colorPiece0=ColorReflection(0,1)               #Color of the 0 pieces
        self.colorPieceX=ColorReflection(0,1)               #Color of the X pieces
        self.colorPiecePlus=ColorReflection(0,1)            #Color of the plus pieces
        self.colorPieceMinus=ColorReflection(0,1)           #Color of the Minus pieces
        self.colorLineInterception=ColorReflection(35,45)   #tabuleiro oficial
        #self.colorLineInterception=Color(70,95)  # casa
        self.colorLine=ColorReflection(0,1)                 #Color of the line
        self.colorStatus=ColorReflection(0,1)               #Current color status

class ColorsRGB:

    __instance = None
    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = ColorsRGB()
        
        return cls.__instance
    
    def __init__(self):
        # self.colorPiece0=ColorsRGB((r,g,b),(r,g,b))               #Color of the 0 pieces
        # self.colorPieceX=ColorsRGB(0,0,1,1,2,2)             #Color of the X pieces
        # self.colorPiecePlus=ColorsRGB(0,0,1,1,2,2)         #Color of the plus pieces
        # self.colorPieceMinus=ColorsRGB(0,0,1,1,2,2)           #Color of the Minus pieces
        self.colorLineInterception=ColorRGB(RGB(20,15,1),RGB(45,35,25))   #tabuleiro oficial
        #self.colorLineInterception=Color(70,95)  # casa
        # self.colorLine=ColorColorsRGB(0,0,1,1,2,2)                #Color of the line
        # self.colorStatus=Color(0,1)     