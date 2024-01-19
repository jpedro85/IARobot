class TreeNode:

    def __init__(self,value , parent = None):
        self.parent = parent
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):
        return self.value
class Tree:

    def __init__(self):
        self.head = TreeNode(None)
        self.length = 0

    def addValue(self,value):

        if(self.length == 0):
            self.head.value = value
            self.length = 1
        else:
            node = self.head
            while(node):
                if(value <= node.value):
                    if (node.left):
                        node = node.left
                    else:
                        node.left = TreeNode(value,node)     
                        self.length+=1
                        break
                else:
                    if (node.right):
                        node = node.right
                    else:
                        node.right = TreeNode(value,node)     
                        self.length+=1 
                        break

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
        else:
            node = self.head
            while(node):
                if(node.left):
                    node = node.left
                else:
                    if(node.parent):
                        node.parent.left = node.right
                        if(node.right):
                            node.right.parent = node.parent
                    else:
                        self.head = node.right if(node.right) else TreeNode(None)
                    self.length -= 1
                    return node.value
                
    def popHigherValue(self):

        if(self.length == 0):
            return None
        else:
            node = self.head
            while(node):
                if(node.right):
                    node = node.right
                else:
                    if(node.parent):
                        node.parent.right = node.left
                        if(node.left):
                            node.left.parent = node.parent
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
        
    def getNodeByIndex2(self,index):

        if(index >= self.length or index < 0):
            raise IndexError
        else:
            
            currentNode = self.head
            i = -1
            b = False
            while(currentNode):
                
                while(currentNode.left and not b):
                    currentNode = currentNode.left
                    
                if(currentNode.right):
                    currentNode = currentNode.right
                else:
                    if(currentNode.parent):
                        pass
    
    def getValueByIndex(self,index):

        if(index >= self.length or index < 0):
            raise IndexError
        else:
            
            current = self.head
            i=0

            while current is not None:

                if(i == index):
                    return current.value
                
                if current.left is None:
                    i+=1
                    current = current.right
                else:
                    # Find the in-order predecessor (rightmost node in the left subtree)
                    predecessor = current.left
                    while predecessor.right is not None and predecessor.right != current:
                        predecessor = predecessor.right

                    if predecessor.right is None:
                        predecessor.right = current  # Link to the current node
                        current = current.left
                    else:
                        predecessor.right = None  # Revert the link
                        i+=1
                        current = current.right
                    

    def printOrderRecur(self):
        def traversal(node):
            if node:
                traversal(node.left)
                print(node.value, end=" ")
                traversal(node.right)

        traversal(self.head)
        print()

    def printOrder(self) -> str:
        current = self.head
        string = ""
        while current is not None:

            if current.left is None:
                string += str(current.value) + " "
                current = current.right
            else:
                # Find the in-order predecessor (rightmost node in the left subtree)
                predecessor = current.left
                while predecessor.right is not None and predecessor.right != current:
                    predecessor = predecessor.right

                if predecessor.right is None:
                    predecessor.right = current  # Link to the current node
                    current = current.left
                else:
                    predecessor.right = None  # Revert the link
                    string += str(current.value) + " "
                    current = current.right

        string += "\n"

        return string

    def print_tree(self):
        def print_tree_recursive(node, depth=0):
            if node:
                print_tree_recursive(node.left, depth + 1)
                print("     " * depth + str(node.value))
                print_tree_recursive(node.right, depth + 1)

        print_tree_recursive(self.head)
        print()