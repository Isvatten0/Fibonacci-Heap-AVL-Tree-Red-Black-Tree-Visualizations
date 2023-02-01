# Created By Team 6: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker
#TODO: delete()

class AVLnode:
    def __init__(self, key):
        self.key = key
        self.height = 1 #Height of 1 is a leaf
        self.left = None #left child
        self.right = None #right child



class AVLtree:
    def __init__(self, tolerance):
        self.root = None
        self.tolerance = tolerance #How much imbalance is acceptable
        self.negTolerance = 0 - tolerance

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
        if self.root == None:
            self.root = AVLnode(key)
            return self.root

        ancestors = [] #Stack that holds ancestors of inserted key. This is needed to update height and rotate

        node = self.root
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

            if nextAncestor == self.root:
                self.root = self.rotate(nextAncestor)
            else:
                parent = self.findParent(nextAncestor.key)
                if parent.left == nextAncestor:
                    parent.left = self.rotate(nextAncestor)
                else:
                    parent.right = self.rotate(nextAncestor)

        return node

    def find(self, key):
        node = self.root
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
        if self.root == None:
            return None
        node = self.root
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

    def delete(self, key): #IMPLEMENT
        return key

def printTree(node: AVLnode): #Debug function to see what the tree looks like on the terminal
    if node != None: 
        leftKey = None
        rightKey = None

        if node.left != None:
            leftKey = node.left.key
        if node.right != None:
            rightKey = node.right.key

        print("(", node.height, ") ", node.key, ": ",  leftKey, ", ", rightKey)
        printTree(node.left)
        printTree(node.right)



if __name__ == "__main__": #Testing environment
    tree = AVLtree(2)
    tree.insert(15)
    print("--15--")
    printTree(tree.root)
    tree.insert(10)
    print("--10--")
    printTree(tree.root)
    tree.insert(30)
    print("--30--")
    printTree(tree.root)
    tree.insert(25)
    print("--25--")
    printTree(tree.root)
    tree.insert(26)
    print("--26--")
    printTree(tree.root)
    tree.insert(27)
    print("--27--")
    #tree.root.right = tree.rotateRight(tree.find(30))
    printTree(tree.root)
