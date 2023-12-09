from Color import *
from utils import *

class ColorsReflection:

    __instance = None
    @classmethod
    def getInstance(cls):
        if(cls.__instance == None):
            cls.__instance = ColorsReflection()
        
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
        self.colorPiece0 = ColorRGB(RGB(0,0,50),RGB(0,0,100))            #Yellow
        self.colorPieceX = ColorRGB(RGB(0,0,50),RGB(0,0,100))            #Pink
        self.colorPiecePlus = ColorRGB(RGB(0,0,50),RGB(0,0,100))         #Green
        self.colorPieceMinus = ColorRGB(RGB(0,0,50),RGB(0,0,100))        #Blue
        self.colorLineInterception = ColorRGB(RGB(34,4,2),RGB(55,9,6))    #Red
        self.colorLine = ColorRGB(RGB(0,0,0),RGB(10,10,10))               #Black
        self.colorStatus = ColorRGB(RGB(0,0,0),RGB(10,10,10))             #Black  