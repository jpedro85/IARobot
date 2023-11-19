class Point:
    # Point constructor
    def __init__(self, xCoords, yCoords, piece):
        self.xCoords = xCoords
        self.yCoords = yCoords
    
    # ToString function to parse the object to a string
    def __str__(self):
        return f"X: {self.xCoords}, Y: {self.yCoords}"
