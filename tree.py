class TreeNode:

    def __init__(self,value , parent = None):
        self.parent = parent
        self.left = None
        self.right = None
        self.value = value

class Tree:

    def __init__(self):
        self.head = TreeNode(None)
        self.length = 0

    def addValue(self,value):

        def addValueRecur(node:TreeNode,value):
            if(value > node.value):
                if(node.right):
                    addValueRecur(node.right,value)
                else:
                    node.right = TreeNode(value,node)
                    self.length+=1
            else:
                if(node.left):
                    addValueRecur(node.left,value)
                else:
                    node.left = TreeNode(value,node)
                    self.length+=1

        if(self.length == 0):
            self.head.value = value
            self.length+=1
        else:
            addValueRecur(self.head,value)

    def getNodeWithLowestValue(self):

        if(self.length == 0):
            return None
        else:

            node = self.head
            while(node):
                if(node.left):
                    node = node.left
                else:
                    return node.value

    def popLowestValue(self):

        if(self.length == 0):
            return None
        elif(self.length == 1):
            return self.head.value
        else:
            node = self.head
            while(node):
                if(node.left):
                    node = node.left
                else:
                    if(node.parent):
                        node.parent.left = node.right
                    else:
                        self.head = node.right if(node.right) else TreeNode(None)
                    self.length -= 1
                    return node.value
                
    def popHigherValue(self):

        print(self.length)
        if(self.length == 0):
            return None
        else:
            node = self.head
            print(node.value)
            while(node):
                if(node.right):
                    node = node.right
                else:
                    if(node.parent):
                        node.parent.right = node.left
                    else:
                        self.head = node.left if(node.left) else TreeNode(None)
                    self.length -= 1
                    return node.value
                
    def getNodeWithHigherValue(self):

        if(self.length == 0):
            return None
        else:
            node = self.head
            while(node):
                if(node.right):
                    node = node.right
                else:
                    return node.value
        
    def getNodeByIndex(self,index):

        def getNodeByIndexRecur(node:TreeNode,actual,index=index):
            
            if(actual == index):
                return node.value
            else:
                value = None
                if(node.left):
                    value = getNodeByIndexRecur(node.left,actual+1,index=index)
                
                if(not value and node.right):
                    value = getNodeByIndexRecur(node.left,actual+1,index=index)

                    if(not value):
                        raise IndexError
                    else:
                        return value
                else:
                    raise IndexError
                
                
        return getNodeByIndexRecur(self.head,0,index=index)