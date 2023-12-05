class RGB:

    def __init__(self,R,G,B):
        self.R = R
        self.G = G
        self.B = B
class ColorReflection:
      #color received by the color sensor (sensor needs to be added!!!!)

    def __init__(self, min,max):
        self.__min= min
        self.__max= max


    def isColorReflection(self,sensorReflection):
        if(self.__minReflex <= sensorReflection <= self.__maxReflex):
            return True                    #if the color is between return true
        else:
            return False                   #if the color is outside the accepted values returns false
        

class ColorRGB:
    
    def __init__(self, RGBmin,RGBmax):
        self.__min=RGBmin
        self.__max=RGBmax
    
    def isColorRgb(self,sensorRgb):
        if(self.__min.R <= sensorRgb[0] <= self.__max.R
           and self.__min.G <= sensorRgb[1] <= self.__max.G
           and self.__min.B <= sensorRgb[2] <= self.__max.B):
            return True
        else:
            return False    
        
    def __str__(self):
        return "Color:"+ str(self.__min.R) + ","+ str(self.__min.G) + ","+ str(self.__min.B) +","