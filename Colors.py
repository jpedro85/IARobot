from Color import *

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
        self.colorPiece0 = ColorRGB(RGB(58,38,25),RGB(86,63,38))          #Yellow
        self.colorPieceX = ColorRGB(RGB(35,3,1),RGB(54,7,5))              #Red
        self.colorPiecePlus = ColorRGB(RGB(15,38,17),RGB(18,44,21))       #Green
        self.colorPieceMinus = ColorRGB(RGB(6,26,48),RGB(8,33,58))        #Blue
        self.colorLineInterception = ColorRGB(RGB(30,4,2),RGB(55,9,6))    #Red Another Type
        self.colorLine = ColorRGB(RGB(0,0,0),RGB(12,16,14))               #Black
        self.colorStatus = ColorRGB(RGB(0,0,0),RGB(12,16,14))             #Black  