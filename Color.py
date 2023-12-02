class Color:
      #color received by the color sensor (sensor needs to be added!!!!)

    def __init__(self, minReflex,maxReflex):
        self.__minReflex=minReflex
        self.__maxReflex=maxReflex


    def isColor(self,sensorReflection):
        #print(sensorReflection) #Verify if the color of the sensor is between the accepted values
        if(self.__minReflex <= sensorReflection <= self.__maxReflex):
            return True                    #if the color is between return true
        else:
            return False                   #if the color is outside the accepted values returns false