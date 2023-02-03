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

    def delete(self, key): #IMPLEMENT
        node = self.root
        ancestors = []
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
        
        nodeToDelete = node
        nodeToReplaceDelete = None
        nodeToRemove = node

        #if it has children, find the replacement. Save it. Find ancestors of replacement. Swap, remove link to the replacement node, and update ancestors
        if nodeToDelete.left != None and nodeToDelete.right != None:
            nodeToReplaceDelete = self.min(nodeToDelete.right)
        elif nodeToDelete.right != None:
            nodeToReplaceDelete = nodeToDelete.right
        elif nodeToDelete.left != None:
            nodeToReplaceDelete = nodeToDelete.left
        else:
            nodeToReplaceDelete = None #no children: find ancestors of key to be deleted. Remove parent's link to deleted node and update ancestors

        if nodeToReplaceDelete != None: #If the node with the key to be deleted had children the node we will remove is the successor
            nodeToRemove = node
        
        node = self.root
        while True:
            if nodeToRemove.key < node.key:
                ancestors.append(node)
                node = node.left
            elif nodeToRemove.key > node.key:
                ancestors.append(node)
                node = node.right
            else:
                break

        parentOfRemovedNode = self.findParent(nodeToRemove.key)
        if nodeToDelete != nodeToRemove:
            self.swap(nodeToDelete, nodeToRemove)

        if parentOfRemovedNode.left == nodeToRemove:
            parentOfRemovedNode.left = nodeToRemove.right
        else:
            parentOfRemovedNode.right = nodeToRemove.right
        
        del nodeToRemove

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

        return None

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


if __name__ == "__main__":
    tree = AVLtree(1)
    tree.insert(20)
    tree.insert(15)
    tree.insert(25)
    tree.insert(14)
    tree.insert(24)
    tree.insert(16)
    tree.insert(26)
    tree.insert(13)
    tree.insert(23)
    printTree(tree.root)
    print("Delete phase")
    tree.delete(13)
    tree.delete(14)
    tree.delete(16)
    printTree(tree.root)
