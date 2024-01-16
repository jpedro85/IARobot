import heapq
from board import Board,Slot
from piece import PieceNone
from Shape import * 
from tree import Tree

class State:

    def __init__(self,board:Board,slot:Slot):
        self.board = board
        self.slot = slot

    def isGoalState(self):
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
                slot.piece = piece
                newBoard.slots[slot.point.x][slot.point.y] = slot

                clearedShapes = newBoard.clearShapes()
                totalPoints = 0
                for key in clearedShapes.keys():
                    totalPoints += 2**(clearedShapes[key])

                successorsStates.append( ( State(newBoard,slot) , totalPoints ) )

        return successorsStates

    def getHeuristicValue(self):

        value = 0
        dicCountPieces = self.board.countPieces()

        dic2 = self.board.countShapes2()

        if(dic2["-"]["Count"] > 0):
            dicCountPieces["-"] -= dic2["-"]["m"]
            value += dic2["-"]["total"]
        
        if(dic2["+"]["Count"] > 0):
            dicCountPieces["+"] -= dic2["+"]["m"]
            value += dic2["-"]["total"]

        if(dic2["X"]["Count"] > 0):
            dicCountPieces["X"] -= dic2["X"]["m"]
            value += dic2["-"]["total"]

        if(dic2["O"]["Count"] > 0):
            dicCountPieces["O"] -= dic2["O"]["m"]
            value += dic2["-"]["total"]

        dicPossibleShapes = { "-" : None , "+" : None , "X" : None , "O" : None }
        dicPossibleShapes["-"] = ShapeMinus.getInstance().getAllPossibleShapes(dicCountPieces["-"])
        dicPossibleShapes["+"] = ShapePlus.getInstance().getAllPossibleShapes(dicCountPieces["+"])
        dicPossibleShapes["X"] = ShapeX.getInstance().getAllPossibleShapes(dicCountPieces["X"])
        dicPossibleShapes["O"] = ShapeO.getInstance().getAllPossibleShapes(dicCountPieces["O"])

        added_Minus = False
        added_Plus = False
        added_X = False
        added_O = False
        for side in range(self.board.size,1,-1):

            if( dicPossibleShapes["-"] and dicPossibleShapes["-"].get(side) and dicPossibleShapes["-"].get(side).get("NShapes") > 0 and not added_Minus ):
                value += 2**(dicPossibleShapes["-"][side]["Points"])
                added_Minus = True
            
            if( dicPossibleShapes["+"] and dicPossibleShapes["+"].get(side) and dicPossibleShapes["+"].get(side).get("NShapes") > 0 and not added_Plus ):
                value += 2**(dicPossibleShapes["+"][side]["Points"])
                added_Plus = True
            
            if( dicPossibleShapes["X"] and dicPossibleShapes["X"].get(side) and dicPossibleShapes["X"].get(side).get("NShapes") > 0 and not added_X ):
                value += 2**(dicPossibleShapes["X"][side]["Points"])
                added_X = True
            
            if( dicPossibleShapes["O"] and dicPossibleShapes["O"].get(side) and dicPossibleShapes["O"].get(side).get("NShapes") > 0 and not added_O ):
                value += 2**(dicPossibleShapes["O"][side]["Points"])
                added_O = True

            if( added_Minus and added_Plus and added_X and added_O ):
               break
        
        return value
        
    
class Node:

    def __init__(self, state:State , total_Points:int , heuristicPoints:int , parent=None):
        self.state = state
        self.parent = parent
        self.total_Points =  total_Points   # Cost to reach this node
        self.heuristicPoint = heuristicPoints  # Estimated Points
        self.expectedPoints = self.total_Points + self.heuristicPoint  # Estimated total Points
        self.removedChildBestExpectedPoints = None

    def __lt__(self, other):
        return self.expectedPoints < other.expectedPoints 
    
    def __gt__(self, other):
        return self.expectedPoints > other.expectedPoints
    
    def compare(self, other):
        """
        returns -1 if self is worse value, 1 if is better value and 0if is equal value  
        """
        return 1 if(self.expectedPoints > other.expectedPoints) else -1 if(self.expectedPoints < other.expectedPoints) else 0

class SMA:

    @classmethod    
    def start(cls,initial_state:State, memory_limit:int):

        initial_node = Node(initial_state, 0, initial_state.getHeuristicValue())
        frontier = Tree()
        frontier.addValue(initial_node)

        while frontier:
            node = frontier.popHigherValue()

            if node.state.isGoalState() :
                return cls.reconstructPath(node)

            for successorState, total_Points in node.state.getSuccessorsStates():
                successor_node = Node(successorState, node.total_Points + total_Points, successorState.getHeuristicValue(),node)
                frontier.addValue(successor_node)
                
                if frontier.length > memory_limit:
                    cls.prune(frontier)

        return None  
    
    @classmethod 
    def reconstructPath(cls,node:Node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
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



    

        
    
