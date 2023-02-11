import time
import threading
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
        self.displayArray = [] #Holds tuples of the form (key, oval, text, positionIndex)
        self.treeRoot = None #Nodes currently in the tree
        self.nodeSize = 30 #Diameter of a node
        self.tolerance = tolerance #How much imbalance is acceptable
        self.negTolerance = 0 - tolerance
        self.treeNeedsMove = False
        #Node object settings
        self.font = 'Helvetica 15 bold'
        self.baseColor = "tan"
        self.highlightColor = "yellow"
        self.rotateColor = "red"
        self.foundColor = "green"
        #Animation Settings
        self.sleepTime = 1
        #Build Main Containers
        self.treeCanvas = tk.Canvas(self.window,width=self.treeCanvasWidth,height=self.treeCanvasHeight,bg="white",relief=tk.RAISED,bd=8)
        self.frame = tk.Frame(self.window)
        self.entry = tk.Entry(self.frame, bd=5)
        self.entryLabel = tk.Label(self.frame, text="Enter node key: ")
        self.insertButton = tk.Button(self.frame, text="Insert", command= lambda: self.insert())
        self.deleteButton = tk.Button(self.frame, text="Delete", command = lambda: self.delete())
        self.findButton = tk.Button(self.frame, text="Find", command = lambda: self.find())
        
        #Place Main Containers
        self.treeCanvas.place(x=0,y=200)
        self.frame.pack()
        self.entryLabel.pack()
        self.entry.pack()
        self.insertButton.pack()
        self.deleteButton.pack()
        self.findButton.pack()
        
        self.definepositions()

        #Place Secondary Items
        #self.drawtree(self.treeRoot)
        self.colornode(self.findobject(8), "yellow")

        #self.treeCanvas.create_line(self.treePositions[0], self.treePositions[1], width = 5, fill = "black")
        
        
    #Animation Functions
    def definepositions(self): #Creates a set of predefined valid positions for the tree nodes to appear on the canvas
        for i in range(1, 7):
            for x in range(1, pow(2, i - 1) + 1):
                self.treePositions.append(((x*2 - 1)*self.treeCanvasWidth/(pow(2, i)), i*self.treeCanvasHeight/6 - 100))
            
        
    def getnodecoord(self, position):
        return (position[0] - self.nodeSize/2, position[1] - self.nodeSize/2, position[0] + self.nodeSize/2, position[1] + self.nodeSize/2)

    def colornode(self, object, color: str):
        if object != None:
            self.treeCanvas.itemconfig(object[1], fill = color)
            return True
        else:
            return False

    def findobject(self, key): #Find tuple holding the canvas objects corresponding to the key
        for tuple in self.displayArray:
            if tuple[0] == key:
                return tuple
        return None

    def moveobject(self, object, index):
        oval = object[1]
        text = object[2]
        self.treeCanvas.coords(oval, self.getnodecoord(self.treePositions[index]))
        self.treeCanvas.coords(text, self.getcoord(self.treePositions[index]))
        self.window.update()

    def movetree(self):
        if self.treeNeedsMove:
            time.sleep(self.sleepTime)
            self.treeNeedsMove = False
            for tuple in self.displayArray:
                newIndex = self.getpositionindex(tuple[0])
                self.moveobject(tuple, newIndex)


    def createnodeobject(self, key, index):
        oval = self.treeCanvas.create_oval(self.getnodecoord(self.treePositions[index]), fill=self.baseColor)
        text = self.treeCanvas.create_text(self.getcoord(self.treePositions[index]), fill="black", text= str(key), font=self.font)
        self.displayArray.append((key, oval, text, index))

    def deletenodeobject(self, object):
        self.treeCanvas.delete(object[1])
        self.treeCanvas.delete(object[2])
        index = 0
        arrayLength = len(self.displayArray)
        while self.displayArray[index][0] != object[0] and index < arrayLength:
            index = index + 1
        self.displayArray.pop(index)

    def getcoord(self, position):
        return (position[0], position[1])

    def getpositionindex(self, key):
        index = 0
        node = self.treeRoot
        while True:
            if node == None:
                return None
            else:
                if key == node.key:
                    return index
                elif key < node.key:
                    node = node.left
                    index = self.lchildindex(index)
                else:
                    node = node.right 
                    index = self.rchildindex(index)

    def parentindex(self, posIndex: int):
        return int((posIndex - 1)/2)
    def lchildindex(self, posIndex: int):
        return int(posIndex * 2 + 1)
    def rchildindex(self, posIndex: int):
        return int(posIndex * 2 + 2)

    #AVL Data Structure Functions

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
        self.treeNeedsMove = True
        leftNode = node.left
        centerNode = node.left.right
        self.colornode(self.findobject(node.key), self.rotateColor)
        self.window.update()
        time.sleep(self.sleepTime)

        leftNode.right = node
        node.left = centerNode

        self.colornode(self.findobject(node.key), self.baseColor)
        self.window.update()
        
        self.updateHeight(node)
        self.updateHeight(leftNode)
        return leftNode

    def rotateLeft(self, node: AVLnode):
        self.treeNeedsMove = True
        rightNode = node.right
        centerNode = node.right.left
        self.colornode(self.findobject(node.key), self.rotateColor)
        self.window.update()
        time.sleep(self.sleepTime)

        rightNode.left = node
        node.right = centerNode
        self.colornode(self.findobject(node.key), self.baseColor)
        self.window.update()

        self.updateHeight(node)
        self.updateHeight(rightNode)
        #self.movetree() #test
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


    def insert(self):
        key=int(self.entry.get())
        if self.treeRoot == None:
            self.treeRoot = AVLnode(key)
            self.createnodeobject(key, 0)
            time.sleep(self.sleepTime)
            self.window.update()
            return self.treeRoot

        ancestors = [] #Stack that holds ancestors of inserted key. This is needed to update height and rotate

        node = self.treeRoot
        index = 0 
        while True:  #Exact same insertion algorithm for a basic bst
            self.colornode(self.findobject(node.key), self.highlightColor)
            self.window.update()
            time.sleep(self.sleepTime)
            self.colornode(self.findobject(node.key), self.baseColor)
            self.window.update()
            if key == node.key:
                return node
            elif key < node.key:
                ancestors.append(node)
                if node.left == None:
                    node.left = AVLnode(key)
                    self.createnodeobject(key, self.lchildindex(index)) 
                    break
                else:
                    node = node.left
                    index = self.lchildindex(index) 
            else:
                ancestors.append(node)
                if node.right == None:
                    node.right = AVLnode(key)
                    self.createnodeobject(key, self.rchildindex(index)) 
                    break
                else:
                    node = node.right
                    index = self.rchildindex(index)
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
            self.movetree()

        return node

    def find(self):
        key=int(self.entry.get())
        node = self.treeRoot
        while True:
            if node == None:
                return None
            else:
                
                if key == node.key:
                    self.colornode(self.findobject(node.key), self.foundColor)
                    self.window.update()
                    time.sleep(self.sleepTime)
                    self.colornode(self.findobject(node.key), self.baseColor)
                    return node
                else:
                    self.colornode(self.findobject(node.key), self.highlightColor)
                    self.window.update()
                    time.sleep(self.sleepTime)
                    self.colornode(self.findobject(node.key), self.baseColor)
                    if key < node.key:
                        node = node.left
                    else:
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
        obj1 = self.findobject(node1.key)
        obj2 = self.findobject(node2.key)
        self.treeCanvas.itemconfig(obj1[2], text=str(node2.key))
        self.treeCanvas.itemconfig(obj2[2], text=str(node1.key))

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

    def delete(self):
        key=int(self.entry.get())
        node = self.treeRoot
        ancestors = []
        numberOfChildren = 0 #Determines delete case
        #find the node with the key to be deleted. Save it
        while True:
            self.colornode(self.findobject(node.key), self.highlightColor)
            self.window.update()
            time.sleep(self.sleepTime)
            self.colornode(self.findobject(node.key), self.baseColor)
            self.window.update()
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
            parentOfRemovedNode = self.findParent(nodeToRemove.key)
            if parentOfRemovedNode.left == nodeToRemove:
                parentOfRemovedNode.left = nodeToRemove.right
            else:
                parentOfRemovedNode.right = nodeToRemove.right
            self.swap(nodeToDelete, nodeToRemove)
            self.deletenodeobject(self.findobject(nodeToRemove.key))
            del nodeToRemove
            self.treeNeedsMove = True
            self.movetree()
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
            else:
                self.treeRoot = child
            self.deletenodeobject(self.findobject(nodeToRemove.key))
            del nodeToRemove
            self.treeNeedsMove = True
            self.movetree()
        else: #No children means simply remove the node
            if nodeToRemove != self.treeRoot:
                parentOfRemovedNode = self.findParent(nodeToRemove.key)
                if parentOfRemovedNode.left == nodeToRemove:
                    parentOfRemovedNode.left = None
                else:
                    parentOfRemovedNode.right = None
            else:
                self.treeRoot = None
            self.deletenodeobject(self.findobject(nodeToRemove.key))
            del nodeToRemove
            self.treeNeedsMove = True
            self.movetree()
            

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
            self.movetree()

        return None

    
if __name__ == "__main__":
    window = tk.Tk()
    window.title("AVL Tree Visualization")
    window.geometry("1920x1080")
    window.maxsize(1920,1080)
    window.minsize(1920,1080)
    window.config(bg="grey")
    AVL_Display(window, 1)
    window.mainloop()
