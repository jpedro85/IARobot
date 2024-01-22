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
                # totalPoints = 0
                # for key in clearedShapes.keys():
                #     totalPoints += 2**(clearedShapes[key])
                totalPoints = sum(2 ** clearedShapes[key] for key in clearedShapes)

                successorsStates.append( ( State(newBoard,newBoard.slots[slot.point.x][slot.point.y]) , totalPoints ) )

        # for state in successorsStates:
        #     print(state[0].slot)

        return successorsStates
    
    def getHeuristicValue(self):

        value = 0
        Left = 0
        dicCountPieces:dict = self.board.countPieces()
        dicBestShape = self.board.getBestShapeForEachShape(dicCountPieces)

        # Consolidate repetitive logic for shape types
        for shape_type in ["-", "+", "X", "O"]:
            best_shape = dicBestShape.get(shape_type)
            if best_shape and best_shape.get("side") != 0:
                dicCountPieces[shape_type] = best_shape["left"]
                value += best_shape["points"]

        dicPossibleShapes = {
            "-": ShapeMinus.getInstance().getAllPossibleShapes(dicCountPieces["-"]),
            "+": ShapePlus.getInstance().getAllPossibleShapes(dicCountPieces["+"]),
            "X": ShapeX.getInstance().getAllPossibleShapes(dicCountPieces["X"]),
            "O": ShapeO.getInstance().getAllPossibleShapes(dicCountPieces["O"])
        }

        added_BestShape = {"-": False, "+": False, "X": False, "O": False}

        for side in range(self.board.size, 1, -1):
            for shape_type in ["-", "+", "X", "O"]:
                if not added_BestShape[shape_type]:
                    shape_data = dicPossibleShapes[shape_type].get(side)
                    if shape_data and shape_data.get("NShapes") > 0:
                      #  value += shape_data["Points"] #! comment or not comment
                        Left += shape_data["Left"]
                        added_BestShape[shape_type] = True
            
            if all(added_BestShape.values()):
                break

        # Add remaining pieces if not added
        for shape_type in ["-", "+", "X", "O"]:
            if not added_BestShape[shape_type]:
                Left += dicCountPieces[shape_type]

        if Left > 0:
            value -= (2**Left)

        #Utils.print( 2 , "sma","heuristic of point " + str(self.slot) + " value:" + str(value) + " Left:" + str(Left) +"\n")
        #Utils.print(2, "sma", f"heuristic of point {self.slot} value: {value} Left: {Left}\n")

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
        #return  (self.depth < other.depth) or (self.expectedPoints < other.expectedPoints) 
    
    def __gt__(self, other):
        return self.expectedPoints > other.expectedPoints
    
    def __eq__(self, other):
        return self.expectedPoints == other.expectedPoints
    
    def __ge__(self, other):
        return self.expectedPoints >= other.expectedPoints
    
    def __le__(self, other):
        return ( self.expectedPoints < other.expectedPoints 
                or (self.expectedPoints == other.expectedPoints and self.depth < other.depth) 
                or (self.expectedPoints == other.expectedPoints and self.depth == other.depth and self.total_Points <= other.total_Points))
        #return  self.expectedPoints <= other.expectedPoints
    
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
        GoalCounter = 0

        while frontier:

            Utils.print(172,"sma","begin iteration:"+str(iter)+" MD:"+str(maxDepth)+" l:"+str(frontier.length)+"\n")
           # Utils.print(153,"sma",frontier.printOrder()+"\n")
            node:Node = frontier.popHigherValue() 

            dif = maxDepth - node.depth
            if(dif > rollBackLimit):  continue


            if node.depth >= 1:
                Utils.print(154,"sma","Start Expanding: "+ str(node)+ " parent:" + str(node.parent) +"\n")
            else:
                Utils.print(154,"sma","Start Expanding: "+ str(node)+"\n")

            if node.state.isGoalState():
                return cls.reconstructPath(node)
            
            actualDepth = node.depth + 1
            maxDepth = actualDepth if (actualDepth > maxDepth) else maxDepth

            for successorState, total_Points in node.state.getSuccessorsStates():

                successor_node = Node(successorState, node.total_Points + total_Points, successorState.getHeuristicValue(),actualDepth,node)
                frontier.addValue(successor_node)
                Utils.print(182,"sma","ActualSuccessorSlot: " + str(successor_node.state.slot)+" HPoints: "+str(successor_node.heuristicPoint)+" TPoints: "+ str(successor_node.total_Points)+" :EPoints: "+str(successor_node.expectedPoints)+" PSlot "+str(successor_node.parent.state.slot)+"\n")

                if frontier.length > memory_limit:
                    cls.prune(frontier)

            iter += 1
            Utils.print(190,"sma","End\n\n\n")

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
        del node