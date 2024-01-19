import heapq
from board import Board,Slot
from piece import PieceNone
from Shape import * 
from tree import Tree
from util import Utils

class State:

    def __init__(self,board:Board,slot:Slot):
        self.board = board
        self.slot = slot

    def isGoalState(self):
        # print("Goal1",len(self.board.pieces) == 0 )
        # print("Gola2",len(self.board.getSlotsWithPiecesOfType(PieceNone)) == 0 )
        return len(self.board.pieces) == 0 or len(self.board.getSlotsWithPiecesOfType(PieceNone)) == 0
    
    def getSuccessorsStates(self):
        """
        returns: [ (state,totalPoints) , ...]
        """
        successorsStates = []
        if len(self.board.pieces) > 0 :

            piece = self.board.pieces.pop(0)
    
            for slot in self.board.getSlotsWithPiecesOfType(PieceNone):
            
                newBoard = self.board.Copy()
                newBoard.slots[slot.point.x][slot.point.y].piece = piece

                clearedShapes = newBoard.clearShapes()
                totalPoints = 0
                for key in clearedShapes.keys():
                    totalPoints += 2**(clearedShapes[key])

                successorsStates.append( ( State(newBoard,newBoard.slots[slot.point.x][slot.point.y]) , totalPoints ) )

        # for state in successorsStates:
        #     print(state[0].slot)

        return successorsStates
    
    def getHeuristicValue(self):

        value = 0
        Left = 0
        dicCountPieces:dict = self.board.countPieces()
        dicBestShape = self.board.getBestShapeForEachShape(dicCountPieces)

        if(dicBestShape.get("-").get("side") != 0):
            dicCountPieces["-"] = dicBestShape["-"]["left"]
            value += dicBestShape["-"]["points"]
        
        if(dicBestShape.get("+").get("side") != 0):
            dicCountPieces["+"] = dicBestShape["+"]["left"]
            value += dicBestShape["+"]["points"]

        if(dicBestShape.get("X").get("side") != 0):
            dicCountPieces["X"] = dicBestShape["X"]["left"]
            value += dicBestShape["X"]["points"]

        if(dicBestShape.get("O").get("side") != 0):
            dicCountPieces["O"] = dicBestShape["O"]["left"]
            value += dicBestShape["O"]["points"]

        dicPossibleShapes = { "-" : None , "+" : None , "X" : None , "O" : None }
        dicPossibleShapes["-"] = ShapeMinus.getInstance().getAllPossibleShapes(dicCountPieces["-"])
        dicPossibleShapes["+"] = ShapePlus.getInstance().getAllPossibleShapes(dicCountPieces["+"])
        dicPossibleShapes["X"] = ShapeX.getInstance().getAllPossibleShapes(dicCountPieces["X"])
        dicPossibleShapes["O"] = ShapeO.getInstance().getAllPossibleShapes(dicCountPieces["O"])

        added_BestShapeMinus = False
        added_BestShapePlus = False
        added_BestShapeX = False
        added_BestShapeO = False
        
        for side in range(self.board.size,1,-1):

            if(not added_BestShapeMinus and dicPossibleShapes["-"] and dicPossibleShapes["-"].get(side) and dicPossibleShapes["-"].get(side).get("NShapes") > 0  ):
                value += dicPossibleShapes["-"][side]["Points"]
                Left += dicPossibleShapes["-"][side]["Left"]
                added_BestShapeMinus = True
            
            if( not added_BestShapePlus and  dicPossibleShapes["+"] and dicPossibleShapes["+"].get(side) and dicPossibleShapes["+"].get(side).get("NShapes") > 0 ):
                value += dicPossibleShapes["+"][side]["Points"]
                Left += dicPossibleShapes["+"][side]["Left"]
                added_BestShapePlus = True
            
            if( not added_BestShapeX and dicPossibleShapes["X"] and dicPossibleShapes["X"].get(side) and dicPossibleShapes["X"].get(side).get("NShapes") > 0 ):
                value += dicPossibleShapes["X"][side]["Points"]
                Left += dicPossibleShapes["X"][side]["Left"]
                added_BestShapeX = True
            
            if( not added_BestShapeO and dicPossibleShapes["O"] and dicPossibleShapes["O"].get(side) and dicPossibleShapes["O"].get(side).get("NShapes") > 0 ):
                value += dicPossibleShapes["O"][side]["Points"]
                Left += dicPossibleShapes["O"][side]["Left"]
                added_BestShapeO = True

            if( added_BestShapeMinus and added_BestShapePlus and added_BestShapeX and added_BestShapeO ):
                break
                    
        if(not added_BestShapeMinus):
            Left += dicCountPieces["-"]

        if(not added_BestShapePlus):
            Left += dicCountPieces["+"]

        if(not added_BestShapeX):
            Left += dicCountPieces["X"]

        if(not added_BestShapeO):
            Left += dicCountPieces["O"]

        teste = value #TODO:delite
        if Left > 0:
            value -= (2**Left)

        Utils.print( 2 , "sma","heuristic of point " + str(self.slot) + " value:" + str(value) + ":" + str(teste) + " Left:" + str(Left) +"\n")

        return value 

    
class Node:

    def __init__(self, state:State , total_Points:int , heuristicPoints:int , depth:int , parent=None):
        self.state = state
        self.parent = parent
        self.total_Points =  total_Points   # Cost to reach this node
        self.heuristicPoint = heuristicPoints  # Estimated Points
        self.expectedPoints = self.total_Points + self.heuristicPoint  # Estimated total Points
        self.removedChildBestExpectedPoints = None
        self.depth = depth

    def __lt__(self, other):
        return self.expectedPoints < other.expectedPoints 
    
    def __gt__(self, other):
        return self.expectedPoints > other.expectedPoints
    
    def __eq__(self, other):
        return self.expectedPoints == other.expectedPoints
    
    def __ge__(self, other):
        return self.expectedPoints >= other.expectedPoints
    
    def __le__(self, other):
        return self.expectedPoints < other.expectedPoints or (self.expectedPoints == other.expectedPoints and self.depth <= other.depth)
    
    def compare(self, other):
        """
        returns -1 if self is worse value, 1 if is better value and 0if is equal value  
        """
        return 1 if(self.expectedPoints > other.expectedPoints) else -1 if(self.expectedPoints < other.expectedPoints) else 0
    
    def __str__(self):
        return "[ D:" + str(self.depth) + ":" + str(self.state.slot) + " Expected:" + str(self.expectedPoints) + " total:" + str(self.total_Points) + "]"

class SMA:

    @classmethod    
    def start(cls,initial_state:State, rollBackLimit:int , memory_limit:int):
        
        maxDepth = 0
        iter =0 
        initial_node = Node(initial_state, 0, initial_state.getHeuristicValue(),maxDepth)
        frontier = Tree()
        frontier.addValue(initial_node)

        while frontier:

            Utils.print(172,"sma","begin iteration:"+str(iter)+"\n")
           # Utils.print(173,"sma",frontier.printOrder())
           # frontier.print_tree()
          #  Utils.print(175,"sma","---------------------------------------------------------------------------------------------\n")
            node:Node = frontier.popHigherValue()
            if(maxDepth - node.depth > rollBackLimit): continue
          #  frontier.print_tree()
            Utils.print(173,"sma","Start Expanding: "+ str(node)+"\n")
           # Utils.print(173,"sma",frontier.printOrder())

            if node.state.isGoalState():
                return cls.reconstructPath(node)
            
            actualDepth = node.depth + 1
            maxDepth = actualDepth if (actualDepth > maxDepth) else maxDepth

            for successorState, total_Points in node.state.getSuccessorsStates():

                successor_node = Node(successorState, node.total_Points + total_Points, successorState.getHeuristicValue(),actualDepth,node)
                frontier.addValue(successor_node)
                
                Utils.print(182,"sma","ActualSuccessorSlot: " + str(successor_node.state.slot)+" HPoints: "+str(successor_node.heuristicPoint)+" TPoints: "+ str(successor_node.total_Points)+" :EPoints: "+str(successor_node.expectedPoints)+" PSlot "+str(successor_node.parent.state.slot)+"\n")

                # if frontier.length > memory_limit:
                #     #TODO: cls.prune(frontier) Uncomment
                #     pass

            iter += 1
            Utils.print(190,"sma","End\n")

        return None  
    
    @classmethod 
    def reconstructPath(cls,node:Node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.pop(len(path)-1)
        return path[::-1]

    @classmethod 
    def prune(cls,frontier:Tree):
    
        node = frontier.popLowestValue()
        if(not node.parent.removedChildBestExpectedPoints):
            node.parent.removedChildBestExpectedPoints = { "state": node.state , "points" : node.expectedPoints }

        elif(node.parent.removedChildBestExpectedPoints["points"] < node.expectedPoints ):
            del node.parent.removedChildBestExpectedPoints
            node.parent.removedChildBestExpectedPoints = { "state": node.state , "points" : node.expectedPoints }
            
        del node