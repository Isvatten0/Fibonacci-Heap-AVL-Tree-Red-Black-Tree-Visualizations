# Created By Team 6: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker


class Node:
    def __init__(self):
        self.key = float('-inf')    # key value
        self.parent = None  # pointer to parent
        self.child = None   # pointer to a child
        self.left = None    # pointer to left sibling
        self.right = None   # pointer to right sibling
        self.degree = 0     # number of children
        self.mark = False   # mark if child has been removed since insertion


class FibonacciHeap:
    def __init__(self):
        self.min = Node()       # pointer to minimum key node
        self.num_nodes = 0      # stores total number of nodes
        self.num_trees = 0      # stores number of nodes in root list
        self.lookup_dict = {}   # dictionary for O(1) search
    
    def _insert_root(self, node):
        self.min.left.right = node
        node.left = self.min.left
        self.min.left = node
        node.right = self.min
        node.parent = None
        self.num_trees += 1
    
    def _remove_root(self, node):
        if(self.min == node):
            if self.min.right != self.min:
                itr = self.min.right
                new_min = 1000
                while(itr != self.min):
                    if(itr.key < new_min):
                        new_min = itr.key
                    itr = itr.right
        node.left.right = node.right
        node.right.left = node.left
        self.num_trees -= 1
    
    def _add_child(self, parent, child):
        # Add child to parents child list
        if parent.child != None:
            child.right = parent.child
            child.left = parent.child.left
            parent.child.left.right = child
            parent.child.left = child
        else:
            parent.child = child
            child.right = child
            child.left = child
        # Make the child's parent 
        child.parent = parent
        # Incrment the parents degree
        parent.degree += 1
    
    # Makes y the child of x. The number of marks of the node also gets updated.
    def _link(self, node_x, node_y):
        self._remove_root(node_x)
        if node_y.mark == True:
            self.marks = False
        self._add_child(node_y, node_x)
        print("y:")
        print(node_y.child.key)

    #First attempt at consolidate. 
    #1. Checks the roots in the list to see if two roots have the same degree.
    #2. Merges the two trees into one root by using the  as the root with the smaller key. The larger key root
    #becomes the child.
    #3 This process is repeated until all roots in the list have different degrees.
    def _consolidate(self):
        
        # for each node in root list
            # check degrees
            # merge if degrees are same
        
        A = [None] * self.num_nodes
        root = self.min
        counter = self.num_trees
        while counter:
            x = root
            root = root.right
            d = x.degree

            # For every root with same degree link
            while A[d]:
                y = A[d]
                if x.key > y.key:
                    x,y = y,x
                self._link(y,x)
                A[d] = None
                d += 1
            A[d] = x
            counter -= 1
        self.min = None
        for i in range(len(A)):
            if A[i]:
                if self.min == None:
                    self.min = A[i]
                else:
                    if A[i].key < self.min.key:
                        self.min = A[i]

    # Cut the node from the tree and place in the root list.
    def _cut(self, node, parent):
        # Cut from child list of parent
        if node == node.right:
            parent.child = None
        else:
            parent.child = node.left
            node.left.right = node.right
            node.right.left = node.left              
        parent.degree =- 1
        # Place in the root list
        self.min.left.right = node
        node.right = self.min
        node.left = self.min.left
        self.min.left = node
        node.parent = None
        node.mark = False
    
    # Cut all parent/grandparent nodes that are marked.
    def _cascade_cut(self, node):
        parent = node.parent
        if parent != None:
            if parent.mark == False:
                parent.mark = True
            else:
                self._cut(node, parent)
                self._cascade_cut(parent)
    
    # Returns the node with the specified key.
    def search(self, key):
        return self.lookup_dict[key]
    
    # Insert a new node into the FibonacciHeap.
    def insert(self, node):
        # Create the new node.
        new_node = Node()
        new_node.key = node
        new_node.left = new_node
        new_node.right = new_node
        # Add the new node to the root list.
        if self.num_nodes == 0:
            self.min = new_node
            self.num_trees += 1
        else:
            self._insert_root(new_node)
            if new_node.key < self.min.key:
                self.min = new_node
        # Add the new node to the lookup_dict.
        self.lookup_dict[new_node.key] = new_node
        # Increment the number of nodes.
        self.num_nodes += 1
    
    # Remove the node from the FibonacciHeap.
    def delete(self, node):
        # Make the node the new min and extract it.
        self.decrease_key(node, 0)
        self.extract_min()
    
    # Return the node with the minimum key.
    def find_min(self):
        return self.min
    
    # Remove and return minimum node from the fibonacci heap
    def extract_min(self):
        # Don't return anything if no nodes
        if self.num_nodes == 0:
            print("No nodes to remove")
            return None
        else:
            # Remove from hash table
            self.lookup_dict.pop(self.min.key)
            # Move each child of minimum key node to root list
            if self.min.child != None:
                itr = self.min.child
                while(itr.parent != None):
                    next = itr.right
                    itr.mark = False
                    self._insert_root(itr)
                    itr = next
            # Set tree as empty or consolidate
            extracted_node = self.min
            self._remove_root(self.min)
            if self.min == self.min.right:
                self.min = Node()
            else:
                self.min = self.min.right
                self._consolidate()
            # Decrement the number of nodes
            self.num_nodes -= 1
            # Return the extracted minimum key node
            return extracted_node
    
    # Concatenate one Fibonacci Heap to another.
    def union(self, other):
        # Skip union if one of the FH is empty.
        if self.num_nodes == 0:
            self.min = other.min
        elif other.num_nodes != 0:
            # Connect the front of first FH to back of second FH and vice versa.
            self.min.left.right = other.min
            other.min.left.right = self.min
            temp = self.min.left
            self.min.left = other.min.left
            other.min.left = temp
            # Change min node if other min key is less than current minimum key.
            if self.min.key > other.min.key:
                self.min = other.min
        # Add other num_trees and num_nodes
        self.num_trees += other.num_trees
        self.num_nodes += other.num_nodes
        # Add other lookups to FH.
        self.lookup_dict.update(other.lookup_dict)
    
    # Decrease the key value of the given node.
    def decrease_key(self, node, newKey):
        # Change the node's key in the lookup_dict.
        self.lookup_dict[newKey] = node
        self.lookup_dict.pop(node.key)
        # Update key value.
        node.key = newKey
        # Cut if node is not in root list and new key is less than parents key.
        if node.parent != None and node.key < node.parent.key:
            self._cut(node, node.parent)
            self._cascade_cut(node.parent)
        # Change min node if new key is less than current minimum key.
        if (node.key < self.min.key):
            self.min = node
    

    # Show full Fibonacci Heap
    def display(self):
        print("TO DO")