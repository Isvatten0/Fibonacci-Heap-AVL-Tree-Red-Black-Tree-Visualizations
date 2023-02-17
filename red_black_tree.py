# Created By Team 6, The Balanced Fibs: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker

# Node Class
class Node() :
    # node constructor
    def __init__(self, value, P, L, R, C):
        self.value = value
        self.parent = P
        self.left_child = L
        self.right_child =R
        self.color = C
        
# Red Black Tree Class
class RBT() :
    # RBT constructor
    def __init__(self):
        self.NULL = Node(0, None, None, None, None)
        self.root = self.NULL
        self.NULL.left_child = None
        self.NULL.right_child = None
        self.NULL.color = "black"
    
    #search method
    def find(self, search_key):
        node = self.root
        match = self.NULL
        while node != self.NULL:                                                   #search tree until end or find match
            if node.value == search_key:
                match = node
                
            if node.value <= search_key:
                node = node.right_child
            else:
                node = node.left_child
        
        if match == self.NULL:                                                     #if no match, return NULL
            #print(search_key, " not in the tree.")
            return self.NULL
        else:
            #print(search_key, " is in the tree.")                                 #if match exists, return node
            return match
    
    #insertion method    
    def insert(self, value):
        search = self.find(value)
        if search != self.NULL:                                                    #if the value exists, don't insert a duplicate
            print("Insertion error:", search.value, "is already in the tree\n")
            return
        
        node = Node(value, None, self.NULL, self.NULL, "red")                      #create an instance of Node
        
        prev_node = None 
        curr_node = self.root
        
        while curr_node != self.NULL:                                              #find correct place in tree
            prev_node = curr_node
            if node.value < curr_node.value:
                curr_node = curr_node.left_child
            else:
                curr_node = curr_node.right_child
        node.parent = prev_node                                                    #once found, set previous as parent
        
        if prev_node == None:                                                      #if the parent is null, node is the root
            self.root = node
            node.color = "black"
            return
        elif node.value < prev_node.value:                                         #else, update previous node's children
            prev_node.left_child = node
        else:
            prev_node.right_child = node
            
        if node.parent.parent == None:                                             #if no grandparent, tree automatically correct
            return                                                                 
        
        self.insertionBalance(node)                                                #else, balance tree
        
    # rotate right, called from insertionBalance
    def rotateRight(self, rotate_node):
        new_top = rotate_node.left_child                                           #left child will be new top
        rotate_node.left_child = new_top.right_child                               #give its right child to rotate node
        if new_top.right_child != self.NULL:
            new_top.right_child.parent = rotate_node
            
        new_top.parent = rotate_node.parent                                        #give rotate node's parent to new top
        if rotate_node.parent == None:                                             #if rotate node was root, new top is root
            self.root = new_top
        elif rotate_node == rotate_node.parent.right_child:                        #if rotate node was right child, new top is the right child
            rotate_node.parent.right_child = new_top
        else:                                                                      #if rotate node was left child, new top is left child
            rotate_node.parent.left_child = new_top
        
        new_top.right_child = rotate_node                                          #rotate node is right child of new top
        rotate_node.parent = new_top                                               #new top is parent of rotate node
        
    # rotate left, called from insertionBalance
    def rotateLeft(self, rotate_node):
        new_top = rotate_node.right_child                                          #right_child child will be new top
        rotate_node.right_child = new_top.left_child                               #give its left_child child to rotate node
        if new_top.left_child != self.NULL:
            new_top.left_child.parent = rotate_node
        
        new_top.parent = rotate_node.parent                                        #give rotate node's parent to new top
        if rotate_node.parent == None:                                             #if rotate node was root, new top is root
            self.root = new_top
        elif rotate_node == rotate_node.parent.left_child:                         #if rotate node was left child, new top is left child
            rotate_node.parent.left_child = new_top
        else:                                                                      #if rotate node was right child, new top is right child
            rotate_node.parent.right_child = new_top                                
        
        new_top.left_child = rotate_node                                           #rotate node is left child of new top
        rotate_node.parent = new_top                                               #new top is parent of rotate node
        
    # fix tree after an insertion, called from insert
    def insertionBalance(self, node):        
        while node.parent.color == "red":                                          #if parent is black, already balanced
            parent = node.parent
            grandparent = node.parent.parent
            
            if parent == grandparent.right_child:                                  #if parent is right child
                uncle = grandparent.left_child
                if uncle.color == "red":                                           #if uncle is also red, color both black & grandparent red
                    uncle.color = "black"
                    parent.color = "black"
                    grandparent.color = "red"
                    node = grandparent                                             #balance tree at grandparent node
                else:                                                              #if uncle is black
                    if node == parent.left_child:                                  #if node is left child, rotate right at parent
                        node = parent
                        self.rotateRight(node)
                    node.parent.color = "black"                                    #color parent black, grandparent red, rotate left at grandparent
                    node.parent.parent.color = "red"
                    self.rotateLeft(node.parent.parent)
            else:                                                                  #if parent is left child
                uncle = grandparent.right_child
                if uncle.color == "red":                                           #if uncle is also red, color both black & grandparent red
                    uncle.color = "black"
                    parent.color = "black"
                    grandparent.color = "red"
                    node = grandparent                                             #balance tree at grandparent node
                else:                                                              #if unlce is black
                    if node == parent.right_child:                                 #if node is right child, rotate left at parent
                        node = parent
                        self.rotateLeft(node)
                        node.parent.color = "black"                                #color parent black, grandparent red, rotate right at grandparent
                        node.parent.parent.color = "red"
                        self.rotateRight(node.parent.parent)
            if node == self.root:                                                  #if you get all the way up to root -> done
                break
        self.root.color = "black"                                                  #color root black
    
    # fix tree after a deletion, called from delete help
    def deletionBalance(self, node):
        while node != self.root and node.color == "black":                         #while not the root & is black
            if node == node.parent.left_child:                                     #if node is left child
                sib = node.parent.right_child
                if sib.color == "red":                                             #if sibling is red, set black, set parent red & rotate left
                    sib.color = "black"
                    node.parent.color = "red"
                    self.rotateLeft(node.parent)
                    sib = node.parent.right_child
                    
                if sib.left_child.color == "black" and sib.right_child.color == "black":    #if sibling's children black, set sib red & parent as node
                    sib.color = "red"
                    node = node.parent
                else:                                                              #else, set both black, sib red & rotate right
                    if sib.right_child.color == "black":
                        sib.left_child.color = "black"
                        sib.color = "red"
                        self.rotateRight(sib)
                        sib = node.parent.right_child
                        
                    sib.color = node.parent.color                                  #fix colors and rotate left on parent
                    node.parent.color = "black"
                    sib.right_child.color = "black"
                    self.rotateLeft(node.parent)
                    node = self.root
            else:                                                                  #if node is right child
                sib = node.parent.left
                if sib.color == "red":                                             #if sibling is red, set black, set parent red & rotate right
                    sib.color = "black"
                    node.parent.color = "red"
                    self.rotateRight(node.parent)
                    sib = node.parent.left_child
                
                if sib.left_child.color == "black" and sib.right_child.color == "black":    #id sibling's children black, set sib red &  parent as node
                    sib.color = "red"
                    node = node.parent
                else:                                                              #else, set both black, sib red & rotate left
                    if sib.left_child.color == "black":
                        sib.right_child.color = "black"
                        sib.color = "red"
                        self.rotateLeft(sib)
                        sib = node.parent.left_child
                    
                    sib.color = node.parent.color                                  #fix colors and rotate right on parent
                    node.parent.color = "black"
                    sib.left_child.color = "black"
                    self.rotateRight(node.parent)
                    node = self.root
        node.color = "black"
        
    # for a node being deleted, move its children up in the tree
    def reassign(self, deleting, moving) :
        if deleting.parent == None:                                                #if deleting node is root
            self.root = moving
        elif deleting == deleting.parent.left_child:                               #if deleting node is left child
            deleting.parent.left_child = moving
        else:                                                                      #is deleting node is right child
            deleting.parent.right_child = moving
        deleting.parent = moving.parent                                            #deleting node's parent is moving node's new parent
     
    # delete a node in the tree given its value 
    def delete(self, search_key) :
        node = self.root
        match = self.NULL
        
        while node != self.NULL:                                                   #search tree until end or find match
            if node.value == search_key:
                match = node
                
            if node.value <= search_key:
                node = node.right_child
            else:
                node = node.left_child
        
        if match == self.NULL:                                                     #if no match, return
            print("Deletion error:", search_key, " not in the tree.\n")
            return
        
        b = match
        b_color = match.color
        if match.left_child == self.NULL:                                          #if the match node has no left child
            a = match.right_child
            self.reassign(match, match.right_child)
        elif match.right_child == self.NULL:                                             #if the match node has no right child
            a = match.left_child
            self.reassign(match, match.left_child)
        else:                                                                      #if the match node has 2 children
            b = self.minimum(match.right_child)
            b_color = b.color
            a = b.right_child
            if b.parent == match:                                                  #if b is the parent of match
                a.parent = b                                                       #set b as the parent of a
            else:
                self.reassign(b, b.right_child)
                b.right_child = match.right_child
                b.right_child.parent = b
            
            self.reassign(match, b)
            b.left_child = match.left_child
            b.left_child.parent = b
            b.color = match.color
            
        if b_color == "black":
            self.deletionBalance(a)
    
    # find minimum node
    def minimum(self, node):
        while node.left_child != self.NULL:
            node = node.left_child
        return node
        
    #just to check tree, delete later       
    def inorder(self, node):
        if node != self.NULL:
            self.inorder(node.left_child)
            print(node.value, " ")
            self.inorder(node.right_child)


#TEST
tree = RBT()

test = tree.find(0)
if(test == tree.NULL):
    print("Search:", test.value, "is NOT in the tree\n")
else:
    print("Search:", test.value, "IS in the tree\n")


tree.insert(77)
tree.insert(2)
tree.insert(22)
tree.insert(77)     #already in tree should print error message
tree.insert(1)
tree.insert(6)
tree.insert(66)
tree.insert(0)
tree.insert(701)

print("Traversal after insertions:")
tree.inorder(tree.root)
print()

test = tree.find(0)
if(test == tree.NULL):
    print("Search:", test.value, "is NOT in the tree\n")
else:
    print("Search:", test.value, "IS in the tree\n")

tree.delete(0)
tree.delete(22)
tree.delete(100)    #not in tree, should print error message

test = tree.find(0)
if(test == tree.NULL):
    print("Search:", test.value, "is NOT in the tree\n")
else:
    print("Search:", test.value, "IS in the tree\n")

print("Traversal after deletions")
tree.inorder(tree.root)
