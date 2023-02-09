import tkinter as tk
class AVLnode:
    def __init__(self, key):
        self.key = key
        self.height = 1 #Height of 1 is a leaf
        self.left = None #left child
        self.right = None #right child


class AVL_Display:
    def __init__(self, root, tolerance):
        self.window = root
        self.treeCanvasWidth = 1920
        self.treeCanvasHeight = 880
        self.treePositions = [] #Possible positions in the tree
        self.displayArray = [] #Holds tuples of the form (Node, oval, text, positionIndex)
        self.treeRoot = None #Nodes currently in the tree
        self.nodeSize = 30 #Diameter of a node
        self.tolerance = tolerance #How much imbalance is acceptable
        self.negTolerance = 0 - tolerance
        #Build Main Containers
        self.treeCanvas = tk.Canvas(self.window,width=self.treeCanvasWidth,height=self.treeCanvasHeight,bg="white",relief=tk.RAISED,bd=8)
        
        #Place Main Containers
        self.treeCanvas.place(x=0,y=200)
        
        self.definepositions()

        #Place Secondary Items
        self.insert(9)
        self.insert(8)
        self.insert(7)
        self.insert(6)
        self.insert(5)
        self.insert(4)
        self.insert(3)
        self.delete(6)
        self.drawtree(self.treeRoot)

        #self.treeCanvas.create_line(self.treePositions[0], self.treePositions[1], width = 5, fill = "black")
        
        
    #Functions to display tree
    def definepositions(self):
        for i in range(1, 7):
            for x in range(1, pow(2, i - 1) + 1):
                self.treePositions.append(((x*2 - 1)*self.treeCanvasWidth/(pow(2, i)), i*self.treeCanvasHeight/6 - 100))

    def drawtree(self, n, i=0):
        index = i
        node = n
        if index >= len(self.treePositions):
            return
        if node.left != None:
            self.treeCanvas.create_line(self.getcoord(self.treePositions[index]), self.getcoord(self.treePositions[self.lchildindex(index)]), fill = "black")
            self.drawtree(node.left,self.lchildindex(index))
            
        if node.right != None:
            self.treeCanvas.create_line(self.getcoord(self.treePositions[index]), self.getcoord(self.treePositions[self.rchildindex(index)]), fill = "black")
            self.drawtree(node.right, self.rchildindex(index))

        oval = self.treeCanvas.create_oval(self.getnodecoord(self.treePositions[index]), fill="brown")
        text = self.treeCanvas.create_text(self.getcoord(self.treePositions[index]), fill="black", text= str(node.key))
        self.displayArray.append((node, oval, text, index))
            
        
    def getnodecoord(self, position):
        return (position[0] - self.nodeSize/2, position[1] - self.nodeSize/2, position[0] + self.nodeSize/2, position[1] + self.nodeSize/2)

    def getcoord(self, position):
        return (position[0], position[1])

    def getHeight(self, node: AVLnode):
        if node == None:
            return 0
        else:
            return node.height

    def updateHeight(self, node: AVLnode):
        maxHeight = max(self.getHeight(node.left), self.getHeight(node.right))
        node.height = maxHeight + 1
    
    def balance(self, node: AVLnode):
        if node == None:
            return 0
        else:
            return self.getHeight(node.left) - self.getHeight(node.right)

    def rotateRight(self, node: AVLnode):
        leftNode = node.left
        centerNode = node.left.right

        leftNode.right = node
        node.left = centerNode
        
        self.updateHeight(node)
        self.updateHeight(leftNode)
        return leftNode

    def rotateLeft(self, node: AVLnode):
        rightNode = node.right
        centerNode = node.right.left

        rightNode.left = node
        node.right = centerNode

        self.updateHeight(node)
        self.updateHeight(rightNode)
        return rightNode

    def rotate(self, node: AVLnode):
        balance = self.balance(node)
        if balance > self.tolerance: 
            if self.balance(node.left) < self.negTolerance + 1:
                node.left = self.rotateLeft(node.left) #LR rotation case
            return self.rotateRight(node) #RR rotation case
        
        if balance <  self.negTolerance:
            if self.balance(node.right) > self.tolerance - 1:
                node.right = self.rotateRight(node.right) #RL rotation case
            return self.rotateLeft(node) #LL rotation case
        return node


    def insert(self, key):
        if self.treeRoot == None:
            self.treeRoot = AVLnode(key)
            return self.treeRoot

        ancestors = [] #Stack that holds ancestors of inserted key. This is needed to update height and rotate

        node = self.treeRoot
        while True:  #Exact same insertion algorithm for a basic bst
            if key == node.key:
                return node
            if key < node.key:
                ancestors.append(node)
                if node.left == None:
                    node.left = AVLnode(key)
                    break
                else:
                    node = node.left
            if key > node.key:
                ancestors.append(node)
                if node.right == None:
                    node.right = AVLnode(key)
                    break
                else:
                    node = node.right
        while len(ancestors): #Go up the tree to update heights and check for unbalanced nodes
            nextAncestor = ancestors.pop()
            self.updateHeight(nextAncestor)

            if nextAncestor == self.treeRoot:
                self.treeRoot = self.rotate(nextAncestor)
            else:
                parent = self.findParent(nextAncestor.key)
                if parent.left == nextAncestor:
                    parent.left = self.rotate(nextAncestor)
                else:
                    parent.right = self.rotate(nextAncestor)

        return node

    def find(self, key):
        node = self.treeRoot
        while True:
            if node == None:
                return None
            else:
                if key == node.key:
                    return node
                if key < node.key:
                    node = node.left
                if key > node.key:
                    node = node.right 

    def findParent(self, key):
        if self.treeRoot == None:
            return None
        node = self.treeRoot
        while True:
            if node.left == None and node.right == None:
                return None
            else:
                if key < node.key:
                    if node.left == None:
                        return None
                    if node.left.key == key:
                        return node
                    node = node.left
                if key > node.key:
                    if node.right == None:
                        return None
                    if node.right.key == key:
                        return node
                    node = node.right

    def swap(self, node1: AVLnode, node2: AVLnode):
        tempKey = node2.key
        node2.key = node1.key
        node1.key = tempKey

    def min(self, node: AVLnode):
        while node.left != None:
            node = node.left
        return node
    
    def max(self, node: AVLnode):
        while node.right != None:
            node = node.right
        return node

    def delete(self, key):
        node = self.treeRoot
        ancestors = []
        numberOfChildren = 0 #Determines delete case
        #find the node with the key to be deleted. Save it
        while True:
            if node == None:
                return node

            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                break
        
        nodeToDelete = node #The node that originally contained the key that needs to be removed. The object could be deleted or key swapped
        nodeToRemove = node #The node that will be deleted and fully removed from the tree

        #if it has two children the node being removed will the be the successor (after swapping keys)
        if nodeToDelete.left != None and nodeToDelete.right != None:
            nodeToRemove = self.min(nodeToDelete.right)
            numberOfChildren = 2
        elif nodeToDelete.left != None or nodeToDelete.right != None:#If it has one child remove the node with the key
            nodeToRemove = nodeToDelete
            numberOfChildren = 1
        else:
            numberOfChildren = 0
        
        node = self.treeRoot
        while True:
            if nodeToRemove.key < node.key:
                ancestors.append(node)
                node = node.left
            elif nodeToRemove.key > node.key:
                ancestors.append(node)
                node = node.right
            else:
                break

        
        if numberOfChildren == 2: #the successor is the replacement so by definition it can only have a right child
            if nodeToRemove != self.treeRoot:
                parentOfRemovedNode = self.findParent(nodeToRemove.key)
                if parentOfRemovedNode.left == nodeToRemove:
                    parentOfRemovedNode.left = nodeToRemove.right
                else:
                    parentOfRemovedNode.right = nodeToRemove.right
            self.swap(nodeToDelete, nodeToRemove)
            del nodeToRemove
        elif numberOfChildren == 1: #One child means move the child up to the parent's place
            child = None
            if nodeToRemove.left != None:
                child = nodeToRemove.left
            else:
                child = nodeToRemove.right
            if nodeToRemove != self.treeRoot:
                parentOfRemovedNode = self.findParent(nodeToRemove.key)
                if parentOfRemovedNode.left == nodeToRemove:
                    parentOfRemovedNode.left = child
                else:
                    parentOfRemovedNode.right = child
            del nodeToRemove
        else: #No children means simply remove the node
            parentOfRemovedNode = self.findParent(nodeToRemove.key)
            if parentOfRemovedNode.left == nodeToRemove:
                parentOfRemovedNode.left = None
            else:
                parentOfRemovedNode.right = None
            del nodeToRemove
            

        while len(ancestors): #Go up the tree to update heights and check for unbalanced nodes
            nextAncestor = ancestors.pop()

            self.updateHeight(nextAncestor)

            if nextAncestor == self.treeRoot:
                self.treeRoot = self.rotate(nextAncestor)
            else:
                parent = self.findParent(nextAncestor.key)
                if parent.left == nextAncestor:
                    parent.left = self.rotate(nextAncestor)
                else:
                    parent.right = self.rotate(nextAncestor)

        return None

    def parentindex(self, posIndex):
        return int((posIndex - 1)/2)
    def lchildindex(self, posIndex):
        return int(posIndex * 2 + 1)
    def rchildindex(self, posIndex):
        return int(posIndex * 2 + 2)

    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("AVL Tree Visualization")
    window.geometry("1920x1080")
    window.maxsize(1920,1080)
    window.minsize(1920,1080)
    window.config(bg="grey")
    AVL_Display(window, 1)
    window.mainloop()
