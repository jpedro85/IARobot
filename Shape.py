from point import *
from piece import *

class Shape:

    def __init__(self):
        self.shapes = {}

    def getPieceNumberFromSideLength(self,sideLength):
        print("Called Shape getPieceNumberFromSideLength")
        return None

    def getAllPossibleShapes(self,numberOfPieces,max=5):
        """
        return { sideLength : numberOfShapes }

        """
        dic = {}
        for side in range(max,1,-1):
            
            n = self.getPieceNumberFromSideLength(side)
            if( n == None ):  
                continue
            else:
                NShapes = numberOfPieces // n 
                Left =  numberOfPieces - (NShapes * n)
                Points = (2**n)*NShapes
                dic.update( { side : { "NShapes" : numberOfPieces // n , "Left" : Left , "Points": Points , "TotalPoints" : Points- (2**Left) } } )

        return dic

    def getShape(self,sideLength):
        if(sideLength in self.shapes.keys() ):
            return self.shapes[sideLength]
        else:
            return None

    def existCompletedShapeBasedOnPoint(slot,board):
        print("Shape has not existCompletedShapeBasedOnPoint! only subclasses")

    def clearCompletedShapeBasedOnPoint(self,slot,board):

        pointArray = self.existCompletedShapeBasedOnPoint(slot,board)

       # if(pointArray):
       #     print("pieceFount")
       #     for p in pointArray:
       #         print(str(p))
       #     print("pieceFount!")

        count = 0
        if(pointArray):
            for point in pointArray:
                board.slots[slot.point.x + point.x][slot.point.y + point.y].piece = PieceNone()
                count += 1

        return count

    def __str__(self):
        
        line = ""
        for key in self.shapes.keys():
            
            line += "\n" + self.shapes[key]

        return line

class ShapePlus(Shape):

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance != None):
            return cls.__instance
        else:
            cls.__instance = ShapePlus()
            return cls.__instance

    def __init__(self):
        super().__init__()

    def existCompletedShapeBasedOnPoint(self,slot,board):
        """
        The function checks if a completed shape exists based on a given point on a board.
        
        :param slot: The "slot" parameter represents a specific slot on the board where a piece can be
        placed. It contains information about the position of the slot, including its x and y
        coordinates
        :param board: The "board" parameter is a variable that represents the game board. It
        contains information about the size of the board and the positions of the slots on the board
        :return: either the pointArray that represent the shape if a completed shape is found, or None if no completed shape is
        found.
        """

        x = slot.point.x
        y = slot.point.y
        N = board.size - x
        if(1 >= y or y >=3 or x >=2):
            N = 3

        if( N >= 3 and  1 <= y <=3  and x<=2):

            for size in range(N,2,-1):
                # print(size)
                # print("atual2" , x , ":" , y)

                if(size%2 != 0):

                    pointArray = self.getShape(size)
                    numberOfPieces = self.getPieceNumberFromSideLength(size)

                    if(pointArray):
                        count = 0
                        for point in pointArray:
                            #print(point)
                            if(type(board.slots[x + point.x][y + point.y].piece.shape) == ShapePlus):
                                count += 1

                        if(count == numberOfPieces):
                            #print("returned")
                            return pointArray

            #print("fffff")
        return None
    
    def getPieceNumberFromSideLength(self,sideLength):

        if(sideLength >= 3 and sideLength % 2 != 0):
            return sideLength*2 -1 
        else:
           # print("Does not exist shape Plus with side {}.".format(sideLength))
            return None
        
    def getShape(self,sideLength):
        """
        The function `getShape` returns a list of points that form a shape called "Plus" with a given
        side length, or None if the shape does not exist.
        
        :param sideLength: The side length of the shape
        :return: list of Point objects representing the shape.
        """
        
        pointArray = super().getShape(sideLength)

        if(pointArray != None):
            return pointArray
        else:

            if(sideLength > 3 and sideLength%2 == 0):
                print("Does not exist shape Plus with side {}.".format(sideLength))
                return None

            pointArray = []

            for i in range(sideLength):
                if( i != sideLength//2):
                    pointArray.append(Point(i,0))   #middle colum except middle point

            for i in  range(-sideLength//2+1,sideLength//2+1):
                pointArray.append(Point(sideLength//2,i)) #middle line 
                
            self.shapes.update({sideLength : pointArray})
            return pointArray
    
    def getAllIncompleteShapeBasedOnPoint(self,board,slot,minPieces:int = 2):
        """
        The function `getAllIncompleteShapeBasedOnPoint` returns a list of incomplete shapes on a board
        based on a given point and minimum number of pieces.
        """
        bestCount = 0
        total = 0
        bestMissing = 0
        
        x = slot.point.x
        y = slot.point.y
        N = board.size - x
        lst = []
        if(1 >= y or y >=3 or x >=2):
            N = 3

        if( N >= 3 and  1 <= y <=3  and x<=2):

            for size in range(N,2,-1):

                if(size%2 != 0):

                    pointArray = self.getShape(size)
                    numberOfPieces = self.getPieceNumberFromSideLength(size)

                    if(pointArray):
                        count = 0
                        countOthers = 0
                        for point in pointArray:
                            if(type(board.slots[x + point.x][y + point.y].piece) == PiecePlus):
                                count += 1
                            elif(type(board.slots[x + point.x][y + point.y].piece) != PieceNone):
                                countOthers += 1

                        if(count >= minPieces and countOthers == 0):
                            missing = numberOfPieces - count
                            lst.append( { "Side" : size, "ActualNumber" : count , "Missing" : missing } )
                            if( bestCount < count):
                                bestCount = count
                                total = numberOfPieces
                                bestMissing = missing

                            if((missing )== 0):
                                bestCount = count
                                total = numberOfPieces
                                bestMissing = missing
                                break

        return lst , bestCount , total , bestMissing




class ShapeMinus(Shape):

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance != None):
            return cls.__instance
        else:
            cls.__instance = ShapeMinus()
            return cls.__instance

    def __init__(self):
        super().__init__()

    def getPieceNumberFromSideLength(self,sideLength):

        if( sideLength == 2 ):
            return 2
        elif( sideLength == 3):
            return 3
        else:
           # print("Does not exist shape Minus with side {}.".format(sideLength))
            return None

    def existCompletedShapeBasedOnPoint(self,slot,board):
        """
        The function checks if there is a completed shape based on a given point on a board.
        
        :param slot: The "slot" parameter is an object that represents a specific slot on the board. It
        contains information about the slot's position and the piece that is currently placed on it
        :param board: The "board" parameter is a variable that represents the game board. It 
        information about the size of the board and the positions of the slots on the board
        :return: either the pointArray if a completed shape is found, or None if no completed shape is
        found.
        """

        x = slot.point.x
        y = slot.point.y

       #print("analizando x:{0} y:{1}".format(x,y))

        N = board.size - y

        if(N == 2):
            max = 2
        else:
            max = 3

        if( N >= 2):
            for size in range(max,1,-1):

                pointArray = self.getShape(size)

              #  if(pointArray):
             #       for p in pointArray:
                        #print(str(p))

                numberOfPieces = self.getPieceNumberFromSideLength(size)
                
                if(pointArray):
                    count = 0
                    for point in pointArray:

                        if(type(board.slots[x + point.x][y + point.y].piece.shape) == ShapeMinus):
                            count += 1

                    if(count == numberOfPieces):
                        #print("returning")
                        return pointArray

        return None

    def getShape(self,sideLength):
        """
        The function `getShape` returns a shape based on the given side length, and if the shape does
        not exist, it prints a message and returns None.
        
        :param sideLength: The side length of the shape
        :return: list of Point objects representing the shape.
        """

        pointArray = super().getShape(sideLength)

        if( pointArray != None):
            return pointArray
        else:

            if(sideLength == 1 or sideLength != 2 and sideLength !=3):
                print("Does not exist shape Minus with side {}.".format(sideLength))

            pointArray = []

            for i in range(sideLength):
                pointArray.append(Point(0,i))
            
            self.shapes.update({sideLength : pointArray})
            return pointArray
        
    def getAllIncompleteShapeBasedOnPoint(self,board,slot,minPieces:int = 2):
        """
        The function `getAllIncompleteShapeBasedOnPoint` returns a list of incomplete shapes on a board
        based on a given point and minimum number of pieces.
        """
        bestCount = 0
        total = 0
        bestMissing = 0

        x = slot.point.x
        y = slot.point.y

        N = board.size - y
        if(N == 2):
            max = 2
        else:
            max = 3

        lst = []
        if( N >= 2):
            for size in range(max,1,-1):

                pointArray = self.getShape(size)
                numberOfPieces = self.getPieceNumberFromSideLength(size)
                
                if(pointArray):
                    count = 0
                    countOthers = 0
                    for point in pointArray:
                        if(type(board.slots[x + point.x][y + point.y].piece) == PieceMinus):
                            count += 1
                        elif(type(board.slots[x + point.x][y + point.y].piece) != PieceNone):
                            countOthers += 1

                    if(count >= minPieces and countOthers == 0):
                        missing = numberOfPieces - count
                        lst.append( { "Side" : size, "ActualNumber" : count , "Missing" : missing } )
                        
                        if(bestCount < count ):
                            bestCount = count
                            total = numberOfPieces
                            bestMissing = missing

                        if((missing )== 0):
                            bestCount = count
                            total = numberOfPieces
                            bestMissing = missing
                            break

        return lst , bestCount , total , bestMissing


class ShapeX(Shape):

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance != None):
            return cls.__instance
        else:
            cls.__instance = ShapeX()
            return cls.__instance

    def __init__(self):
        super().__init__()

    def getPieceNumberFromSideLength(self,sideLength):

        if( sideLength >= 3 and sideLength%2 != 0):
            return sideLength*2 -1 
        else:
            #print("Does not exist shape X with side {}.".format(sideLength))
            return None

    def existCompletedShapeBasedOnPoint(self,slot,board):
        """
        The function checks if there is a completed shape based on a given point on a board.
        
        :param slot: The "slot" parameter is an object that represents a specific slot on the board. It
        contains information about the slot's position and the piece that is currently placed on it
        :param board: The "board" parameter is a variable that represents the game board. It 
        information about the size of the board and the positions of the slots on the board
        :return: either the pointArray if a completed shape is found, or None if no completed shape is
        found.
        """

        x = slot.point.x
        y = slot.point.y

        #print("analizando x:{0} y:{1}".format(x,y))

        NX = board.size - x
        NY = board.size - y
        N = NY if NX > NY else NX

        if(N >= 3):

            for size in range(N,2,-1):

                #print(size)

                if(size%2 != 0):

                    pointArray = self.getShape(size)
                    numberOfPieces = self.getPieceNumberFromSideLength(size)

                    if(pointArray):

                        count = 0
                        for point in pointArray:
                            #print(str(point))

                            if(type(board.slots[x + point.x][y + point.y].piece.shape) == ShapeX):
                                count += 1

                        if(count == numberOfPieces):
                            #print("returning:", numberOfPieces , size)
                            return pointArray

        return None

    def getShape(self,sideLength):
        """
        The function `getShape` returns a list of points that form a shape based on the given side
        length, or None if the shape does not exist.
        
        :param sideLength: The side length of the shape
        :return: ist of Point objects representing the shape.
        """
        
        pointArray = super().getShape(sideLength)

        if(pointArray != None):
            return pointArray
        else:

            if(sideLength > 3 and sideLength%2 == 0):
                print("Does not exist shape X with side {}.".format(sideLength))
                return None

            pointArray = []

            for i in range(sideLength):
                if( i != sideLength//2):
                    pointArray.append(Point(i,i))           #diagonal 1 less middle point
                pointArray.append(Point(i,sideLength-1-i))  #diagonal 2
                
            self.shapes.update({sideLength : pointArray})
            return pointArray


    def getAllIncompleteShapeBasedOnPoint(self,board,slot,minPieces:int = 2):
        """
        The function `getAllIncompleteShapeBasedOnPoint` returns a list of incomplete shapes on a board
        based on a given point and minimum number of pieces.
        """
        bestCount = 0
        total = 0
        bestMissing = 0

        x = slot.point.x
        y = slot.point.y

        NX = board.size - x
        NY = board.size - y
        N = NY if NX > NY else NX

        lst = []
        if(N >= 3):
            for size in range(N,2,-1):
                if(size%2 != 0):

                    pointArray = self.getShape(size)
                    numberOfPieces = self.getPieceNumberFromSideLength(size)

                    if(pointArray):

                        count = 0
                        countOthers = 0
                        for point in pointArray:
                            if(type(board.slots[x + point.x][y + point.y].piece) == PieceX):
                                count += 1
                            elif(type(board.slots[x + point.x][y + point.y].piece) != PieceNone):
                                countOthers += 1

                        if(count >= minPieces and countOthers == 0):
                            missing = numberOfPieces - count
                            lst.append( { "Side" : size, "ActualNumber" : count , "Missing" : missing } )

                            if( bestCount < count):
                                bestCount = count
                                total = numberOfPieces
                                bestMissing = missing

                            if(missing == 0):
                                bestCount = count
                                total = numberOfPieces
                                bestMissing = missing
                                break

        return lst , bestCount , total , bestMissing




class ShapeO(Shape):

    __instance = None

    @classmethod
    def getInstance(cls):
        if(cls.__instance != None):
            return cls.__instance
        else:
            cls.__instance = ShapeO()
            return cls.__instance        

    def __init__(self):
        super().__init__()
        
    def getPieceNumberFromSideLength(self,sideLength):

        if( sideLength >= 2 ):
            return (sideLength**2) - ((sideLength-2)**2)
        else:
            #print("Does not exist shape O with side {}.".format(sideLength))
            return -1

    def existCompletedShapeBasedOnPoint(self,slot,board):
        """
        The function checks if a completed shape exists based on a given point on a board.
        
        :param slot: The "slot" parameter represents a specific slot on the board where a piece can be
        placed. It contains information about the position of the slot, including its x and y
        coordinates
        :param board: The "board" parameter is a variable that represents the game board. It
        contains information about the size of the board and the positions of the slots on the board
        :return: either the pointArray that represent the shape if a completed shape is found, or None if no completed shape is
        found.
        """

        
        x = slot.point.x
        y = slot.point.y

      #  print("analizando x:{0} y:{1}".format(x,y))

        NX = board.size - x
        NY = board.size - y
        N = NY if NX > NY else NX

        if( N >= 2):

            for size in range(N,1,-1):

               # print(size)

                pointArray = self.getShape(size)
                numberOfPieces = self.getPieceNumberFromSideLength(size)


             #   if(pointArray):
              #      for p in pointArray:
               #         print(str(p))

                count = 0
                for point in pointArray:

                    if(type(board.slots[x + point.x][y + point.y].piece.shape) == ShapeO):
                        count += 1

                if(count == numberOfPieces):
                   # print("returning:", numberOfPieces , size)
                    return pointArray


        return None


    def getShape(self,sideLength):
        
        pointArray = super().getShape(sideLength)

        if(pointArray != None):
            return pointArray
        else:

            if(sideLength < 2 ):
                print("Does not exist shape O with side {}.".format(sideLength))
                return None

            pointArray = []

            for i in range(sideLength):
                pointArray.append(Point(0,i))               #fist line

                if( i!= 0 and i != sideLength-1):
                    pointArray.append(Point(i,0))               #fist colum expect first and last point
                    pointArray.append(Point(i,sideLength-1))    #last colum expect first and last point
                
                pointArray.append(Point(sideLength-1,i))    #last line

            self.shapes.update({sideLength : pointArray})
            return pointArray
        
    def getAllIncompleteShapeBasedOnPoint(self,board,slot,minPieces:int = 2):
        """
        The function `getAllIncompleteShapeBasedOnPoint` returns a list of incomplete shapes on a board
        based on a given point and minimum number of pieces.
        """
        bestCount = 0
        total = 0
        bestMissing = 0
        
        x = slot.point.x
        y = slot.point.y

        NX = board.size - x
        NY = board.size - y
        N = NY if NX > NY else NX

        lst = []
        if( N >= 2):
            for size in range(N,1,-1):

                pointArray = self.getShape(size)
                numberOfPieces = self.getPieceNumberFromSideLength(size)

                count = 0
                countOthers = 0
                for point in pointArray:
                    if(type(board.slots[x + point.x][y + point.y].piece) == PieceO):
                        count += 1
                    elif(type(board.slots[x + point.x][y + point.y].piece) != PieceNone):
                        countOthers += 1

                if(count >= minPieces and countOthers == 0):
                    missing = numberOfPieces - count
                    lst.append( { "Side" : size, "ActualNumber" : count , "Missing" : missing } )
                    if( bestCount < count):
                        bestCount = count
                        total = numberOfPieces
                        bestMissing = missing

                    if((missing )== 0):
                        bestCount = count
                        total = numberOfPieces
                        bestMissing = missing
                        break

        return lst , bestCount , total , bestMissing