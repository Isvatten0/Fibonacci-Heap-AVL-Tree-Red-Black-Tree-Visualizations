# Created By Team 6, The Balanced Fibs: Bryson Duckworth, Alyssa Gabrielson, Will Miller, Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker

import time
import threading
import tkinter as tk


class Node:
    def __init__(self):
        self.key = float('-inf')    # key value
        self.parent = None  # pointer to parent
        self.child = None   # pointer to a child
        self.left = None    # pointer to left sibling
        self.right = None   # pointer to right sibling
        self.degree = 0     # number of children
        self.mark = False   # mark if child has been removed since insertion
        self.highlight = False  #Highlight for animation
    

class FibonacciHeap:
    def __init__(self, root: tk.Tk):
        self.min = None         # pointer to minimum key node
        self.num_nodes = 0      # stores total number of nodes
        self.num_trees = 0      # stores number of nodes in root list

        # Window Settings
        self.window = root
        self.treeCanvasWidth = 1920
        self.treeCanvasHeight = 880
        self.nodeSize = 30      #Diameter of a node
        self.visited = {}
        #Node object settings
        self.font = 'Helvetica 15 bold'
        self.baseColor = "tan"
        self.markedColor = "orange"
        self.highlightColor = "yellow"
        self.visitedColor = "red"
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
                new_min = self.min.right
                while(itr != self.min):
                    if(itr.key < new_min.key):
                        new_min = itr
                    itr = itr.right
                self.min = new_min
            else:
                self.min = None
                self.num_trees -= 1
                return
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
    
    # Makes y the child of x.
    def _link(self, node_x, node_y):
        self._remove_root(node_x)
        if node_y.mark == True:
            self.marks = False
        self._add_child(node_y, node_x)

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
                self.treeCanvas.delete('all')
                self.display()
                time.sleep(self.sleepTime)
                self.window.update()
                A[d] = None
                d += 1
            A[d] = x
            counter -= 1

    # Cut the node from the tree and place in the root list.
    def _cut(self, node, parent):
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
        # Cut from child list of parent
        if node == node.right:
            parent.child = None
        else:
            parent.child = node.right
            node.left.right = node.right
            node.right.left = node.left
        parent.degree -= 1
        # Place in the root list
        self.min.left.right = node
        node.right = self.min
        node.left = self.min.left
        self.min.left = node
        node.parent = None
        node.mark = False
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
    
    # Cut all parent/grandparent nodes that are marked.
    def _cascade_cut(self, node: Node):
        if node.parent != None:
            if node.mark == False:
                node.mark = True
            else:
                parent = node.parent
                node.highlight = True
                self._cut(node, parent)
                self.num_trees += 1
                self.treeCanvas.delete('all')
                self.display()
                time.sleep(self.sleepTime)
                self.window.update()
                node.highlight = False
                self._cascade_cut(parent)
    
    # Returns the node with the specified key.
    def find(self, key=None, current_node=None, current_tree=None, current_root=None):
        if key == None:
            key=int(self.entry.get())
        # If find was called, set current tree and node.
        if current_node == None:
            current_tree = self.min
            current_node = self.min
            current_root = self.min
        # Add node to list
        self.visited[current_node.key] = True
        # 1. return if current node is key.
        # 2. find lower.
        # 3. find right.
        if current_node.key == key:
            # Display and return node.
            current_node.highlight = True
            self.treeCanvas.delete('all')
            self.display()
            time.sleep(self.sleepTime)
            self.window.update()
            current_node.highlight = False
            self.visited.clear()
            return current_node
        if current_node.child != None and current_node.key < key:
            self.treeCanvas.delete('all')
            self.display()
            time.sleep(self.sleepTime)
            self.window.update()
            found = self.find(key, current_node.child, current_tree, current_node.child)
            if found != None:
                return found
        if current_node.right != current_root:
            self.treeCanvas.delete('all')
            self.display()
            time.sleep(self.sleepTime)
            self.window.update()
            found = self.find(key, current_node.right, current_tree, current_root)
            if found != None:
                return found
        else:
            self.treeCanvas.delete('all')
            self.display()
            self.window.update()
            return None
    
    # Insert a new node into the FibonacciHeap.
    def insert(self, key = None):
        if key == None:
            if self.entry.get() == '':
                for i in range(1,21):
                    self.insert(i)
                return
            else:
                key = int(self.entry.get())
        # Create the new node.
        new_node = Node()
        new_node.key = key
        new_node.left = new_node
        new_node.right = new_node
        new_node.highlight = True
        # Add the new node to the root list.
        if self.num_nodes == 0:
            self.min = new_node
            self.num_trees += 1
        else:
            self._insert_root(new_node)
            if new_node.key < self.min.key:
                self.min = new_node
        # Increment the number of nodes.
        self.num_nodes += 1
        self.treeCanvas.delete('all')
        self.display()
        new_node.highlight = False
    
    # Remove the node from the FibonacciHeap.
    def delete(self):
        key=int(self.entry.get())
        # Make the node the new min and extract it.
        node = self.find(key)
        if node != self.min:
            self.decrease_key(node, float('-inf'))
        self.extract_min()
    
    # Return the node with the minimum key.
    def find_min(self):
        self.min.highlight = True
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
        self.min.highlight = False
        return self.min
    
    # Remove and return minimum node from the fibonacci heap
    def extract_min(self):
        # Don't return anything if no nodes
        if self.num_nodes == 0:
            print("No nodes to remove")
            return None
        else:
            # Display Min Node Highlighted
            self.min.highlight = True
            # Move each child of minimum key node to root list
            if self.min.child != None:
                itr = self.min.child
                last = itr.left
                while(itr.parent != None):
                    next = itr.right
                    itr.mark = False
                    self._insert_root(itr)
                    itr = next
                    self.min.child = itr
                    itr.left = last
                    itr.highlight = True
                    itr.highlight = False
            # Set tree as empty or consolidate
            extracted_node = self.min
            # Remove the min.
            self._remove_root(self.min)
            self.num_nodes -= 1
            # Consolidate the heap.
            self._consolidate()
            self.treeCanvas.delete('all')
            self.display()
            time.sleep(self.sleepTime)
            self.window.update()
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
    
    # Decrease the key value of the given node.
    def decrease_key(self, node: Node, newKey: int):
        # Display before.
        node.highlight = True
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
        # Update key value.
        node.key = newKey
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
        # Cut if node is not in root list and new key is less than parents key.
        if node.parent != None and node.key < node.parent.key:
            parent = node.parent
            self._cut(node, parent)
            self.num_trees += 1
            self._cascade_cut(parent)
        # Change min node if new key is less than current minimum key.
        if (node.key < self.min.key):
            self.min = node
        # Display after.
        self.treeCanvas.delete('all')
        self.display()
        time.sleep(self.sleepTime)
        self.window.update()
        node.highlight = False
    
    def display(self, current_node=None, x=181, y=100):
        if current_node == None:
            current_node = self.min
            self.treeCanvas.create_text(x+self.nodeSize/2, y+self.nodeSize/2, text="Minimum Node")
            self.treeCanvas.create_line(x+self.nodeSize/2, y+self.nodeSize, x+self.nodeSize/2, y+100, arrow=tk.LAST)
            y = y + 100

        # Draw node.
        if current_node.highlight == True:
            self.treeCanvas.create_oval(x, y, x+self.nodeSize, y+self.nodeSize, fill=self.highlightColor)
        elif self.visited.get(current_node.key):
            self.treeCanvas.create_oval(x, y, x+self.nodeSize, y+self.nodeSize, fill=self.visitedColor)
        elif current_node.mark == True:
            self.treeCanvas.create_oval(x, y, x+self.nodeSize, y+self.nodeSize, fill=self.markedColor)
        else:
            self.treeCanvas.create_oval(x, y, x+self.nodeSize, y+self.nodeSize, fill=self.baseColor)
        self.treeCanvas.create_text(x+self.nodeSize/2, y+self.nodeSize/2, text=current_node.key)
        
        # Draw each linked node.
        current_child = current_node.child
        offset = -self.nodeSize * (2**(current_node.degree-3)) * (current_node.degree-1) / 2

        # if current_child and current_node.key == 1:
        #     print(current_node.degree)
        #     print(" ")
        for child in range(current_node.degree):

            # Draw Parent Links
            self.treeCanvas.create_line(x+self.nodeSize/2, y+self.nodeSize, x+offset+self.nodeSize/2, y+100, arrow=tk.BOTH)

            # Draw Child Node
            self.display(current_child, x+offset, y+100)

            # Draw Sibling Links
            if current_child != current_node.child.left:
                # Draw right line
                offset2 = offset + (2**child * self.nodeSize) + 60
                self.treeCanvas.create_line(x+self.nodeSize+offset, y+115, x+offset2, y+115, arrow=tk.BOTH)
                offset = offset2

            # Iterate child.
            current_child = current_child.right
        
        if current_node.parent == None and current_node.right != self.min:
            tree_offset = (current_node.right.degree+current_node.degree) * 45 + 120
            self.treeCanvas.create_line(x+self.nodeSize, y+self.nodeSize/2, x+tree_offset, y+self.nodeSize/2, arrow=tk.BOTH)
            self.display(current_node.right, x+tree_offset, y)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Fibonacci Heap Visualization")
    window.geometry("1920x1080")
    window.maxsize(1920,1080)
    window.minsize(1920,1080)
    window.config(bg="grey")
    FibonacciHeap(window)
    window.mainloop()
