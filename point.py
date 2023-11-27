class Point:
    # Point constructor
    def __init__(self, xCoords, yCoords):
        self.x = xCoords
        self.y = yCoords
    
    # ToString function to parse the object to a string
    def __str__(self):
        return "(X:{self.x} Y:{self.y})"
