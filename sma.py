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
        dicCountPieces = self.board.countPieces()

        #print(dicCountPieces)
        dic2 = self.board.countShapes2(1)

        if(dic2["-"]["Count"] > 0):
            dicCountPieces["-"] -= dic2["-"]["m"]
            value += dic2["-"]["total"] if (dicCountPieces["-"] >= 0 ) else 0
        
        if(dic2["+"]["Count"] > 0):
         #   print("ADDED",dic2["-"]["total"])
            dicCountPieces["+"] -= dic2["+"]["m"]
            value += dic2["+"]["total"] if (dicCountPieces["+"] >= 0 ) else 0

        if(dic2["X"]["Count"] > 0):
            dicCountPieces["X"] -= dic2["X"]["m"]
            value += dic2["X"]["total"] if (dicCountPieces["X"] >= 0 ) else 0

        if(dic2["O"]["Count"] > 0):
            dicCountPieces["O"] -= dic2["O"]["m"]
            value += dic2["O"]["total"] if (dicCountPieces["O"] >= 0 ) else 0

        #print(dicCountPieces,value)

        dicPossibleShapes = { "-" : None , "+" : None , "X" : None , "O" : None }
        dicPossibleShapes["-"] = ShapeMinus.getInstance().getAllPossibleShapes(dicCountPieces["-"])
        dicPossibleShapes["+"] = ShapePlus.getInstance().getAllPossibleShapes(dicCountPieces["+"])
        dicPossibleShapes["X"] = ShapeX.getInstance().getAllPossibleShapes(dicCountPieces["X"])
        dicPossibleShapes["O"] = ShapeO.getInstance().getAllPossibleShapes(dicCountPieces["O"])

        #print(dicPossibleShapes["-"])

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
    
    def __eq__(self, other):
        return self.expectedPoints == other.expectedPoints
    
    def __ge__(self, other):
        return self.expectedPoints >= other.expectedPoints
    
    def __le__(self, other):
        return self.expectedPoints <= other.expectedPoints
    
    def compare(self, other):
        """
        returns -1 if self is worse value, 1 if is better value and 0if is equal value  
        """
        return 1 if(self.expectedPoints > other.expectedPoints) else -1 if(self.expectedPoints < other.expectedPoints) else 0
    
    def __str__(self):
        return self.state.slot.__str__()

class SMA:

    @classmethod    
    def start(cls,initial_state:State, memory_limit:int):

        initial_node = Node(initial_state, 0, initial_state.getHeuristicValue())
        frontier = Tree()
        frontier.addValue(initial_node)

        while frontier:
            print("begin iteration")
            Utils.getFile().write("begin iteration\n")
            #frontier.print()   
            frontier.print_tree()
            node = frontier.popHigherValue()
            print("Start Expanding:", node.state.slot)
            Utils.getFile().write("Start Expanding: "+ str(node.state.slot)+"\n")

           # print(node.state.board)
           # print("end Before:", node.state.slot)

            if node.state.isGoalState():
                return cls.reconstructPath(node)

            for successorState, total_Points in node.state.getSuccessorsStates():
                successor_node = Node(successorState, node.total_Points + total_Points, successorState.getHeuristicValue(),node)
                frontier.addValue(successor_node)
                
                print("AtualSuccesssorSlot:",successor_node.state.slot,"Hpoints:",successor_node.heuristicPoint,"TPoins:",successor_node.total_Points,":EPoints:",successor_node.expectedPoints,"PSlot",successor_node.parent.state.slot)
                Utils.getFile().write("AtualSuccesssorSlot: " + str(successor_node.state.slot)+" Hpoints: "+str(successor_node.heuristicPoint)+" TPoins: "+ str(successor_node.total_Points)+" :EPoints: "+str(successor_node.expectedPoints)+" PSlot "+str(successor_node.parent.state.slot)+"\n")

                if frontier.length > memory_limit:
                    #cls.prune(frontier) //TODO:Uncoment
                    pass

            print("End")
            Utils.getFile().write("End\n")

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