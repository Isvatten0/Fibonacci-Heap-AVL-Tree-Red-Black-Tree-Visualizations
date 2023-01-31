# Created By Team 6: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker
#TODO: rotateRight(), rotateLeft(), delete()

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

    def getHeight(self, node):
        if node == None:
            return 0
        else:
            return self.height
    
    def updateHeight(self, node):
        maxHeight = max(self.getHeight(node.left), self.getHeight(node.right))
        node.height = maxHeight + 1
    
    def balance(self, node):
        if node == None:
            return 0
        else:
            return self.getHeight(node.left) - self.getHeight(node.right)

    def rotateRight(self, node): #IMPLEMENTATION NEEDED
        return node

    def rotateLeft(self, node): #IMPLEMENTENTATION NEEDED
        return node

    def rotate(self, node):
        balance = self.balance(node)
        if balance > self.tolerance:
            if self.balance(node.left) < 0:
                node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)
        if balance < self.tolerance * -1:
            if self.balance(node.right) > 0:
                node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)
        return node


    def insert(self, key):
        if self.root == None:
            self.root = AVLnode(key)
            return self.root

        node = self.root
        while True:  
            if key == node.key:
                return node
            if key < node.key:
                if node.left == None:
                    node.left = AVLnode(key)
                    break
                else:
                    node = node.left
            if key > node.key:
                if node.right == None:
                    node.right = AVLnode(key)
                    break
                else:
                    node = node.right
        self.updateHeight(node)
        return self.rotate(node)

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
        

    def delete(self, key): #IMPLEMENT
        return key