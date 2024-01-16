class Point:
    # Point constructor
    def __init__(self, xCoords, yCoords):
        self.x = xCoords
        self.y = yCoords
    
    # ToString function to parse the object to a string
    def __str__(self):
        return "(X{0} Y{1})".format(self.x,self.y)
