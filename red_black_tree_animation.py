# Created by the Balanced Fibs: Bryson Duckworth, Alyssa Gabrielson, Will Miller,
#                               Riley Parker, Sydney Pierce, Luke Roberts, & Joey Walker

from tkinter import *
import time

# set the size of the highlight for the nodes
highlight = 4


class Node:
    # Initialized the Node class and its variables
    def __init__(self, value, black, left=None, right=None):
        self.value = value
        self.is_node_nlack = black
        self.left_child = left
        self.right_child = right


class RBT:

    # Initialize recent items with root node or None
    def __init__(self, root=None):
        self.root = root
        self.recentItems = [root.value if root else None, None]

    # Insert value into binary search tree and maintain red-black properties

    def insert(self, value, root):
        root, option = self.insert_node(value, root)
        root.is_node_nlack = True
        self.recentItems.append(None)
        return root

    # Common recursive binary insertion, added balancing for red-black tree
    def insert_node(self, value, root):
        # If the root is None, create a new node for the value and return it as the new root
        if (root == None):
            rootNode = Node(value, False)  # Always insert new nodes as RED
            self.recentItems = [value]
            return rootNode, 1

        # If the value is less than the root's value, insert it in the left subtree
        if (value < root.value):
            root.left_child, option = self.insert_node(value, root.left_child)
            uncle = root.right_child  # Uncle node for the newly inserted node

        # If the value is greater than the root's value, insert it in the right subtree
        elif (value > root.value):
            root.right_child, option = self.insert_node(
                value, root.right_child)
            uncle = root.left_child  # Uncle node for the newly inserted node

        # If the value already exists, do not insert it and set option to 0
        else:
            self.recentItems = []
            return root, 0

        if (option == 1):
            # If the father node is black, no modifications are needed
            if (root.is_node_nlack):
                option = 0

            # If the father node is red, the behavior depends on the uncle node
            else:
                option = 2

        elif (option == 2):
            # If the uncle node is black, balance the tree
            if (self.is_node_nlack(uncle)):
                Balance = self.get_balance(root)
                # Left unbalanced
                if (Balance > 1):
                    # Left-Right option
                    if (value > root.left_child.value):
                        root.left_child = self.rotate_left(root.left_child)
                    root = self.rotate_right(root)

                    # Swap the colors of the root and the uncle node
                    root.right_child, root = self.swap_node_color(
                        root.right_child, root)
                    option = 0  # No further modifications are needed

                # Right unbalanced
                elif (Balance < - 1):

                    # Right-Left option
                    if (value < root.right_child.value):
                        root.right_child = self.rotate_right(root.right_child)

                    root = self.rotate_left(root)
                    # Swap the colors of the root and the uncle node
                    root.left_child, root = self.swap_node_color(
                        root.left_child, root)
                    option = 0  # No further modifications are needed

            else:  # If the uncle node is red, change the colors of the father, uncle, and grandfather nodes
                root.left_child = self.set_node_to_black(root.left_child)
                root.right_child = self.set_node_to_black(root.right_child)
                root = self.set_node_to_red(root)
                option = 1  # The grandfather node becomes a son node in the next iteration

        return root, option

    # Function for rotating nodes to the right
    def rotate_right(self, oldRoot):
        # The left child of the old root becomes the new root
        newRoot = oldRoot.left_child
        # The right child of the new root becomes the left child of the old root
        oldRoot.left_child, newRoot.right_child = newRoot.right_child, oldRoot
        # If the old root was the most recently added node, update the most recent item
        if (oldRoot.value == self.recentItems[0]):
            self.recentItems[0] = newRoot.value
        # Add the values of the old root and its left child to the recent items list
        self.recentItems.extend(
            [oldRoot.value, newRoot.value, oldRoot.left_child])
        return newRoot

        # Rotate left

    def rotate_left(self, oldRoot):
        # Set the new root to be the right child of the old root
        newRoot = oldRoot.right_child
        # Reassign the children of the old and new root to complete the rotation
        oldRoot.right_child, newRoot.left_child = newRoot.left_child, oldRoot
        # If the old root was the most recently inserted node, update the reference in recentItems
        if (oldRoot.value == self.recentItems[0]):
            self.recentItems[0] = newRoot.value
        # Add the relevant nodes to the recentItems list
        self.recentItems.extend(
            [oldRoot.value, newRoot.value, oldRoot.right_child])
        # Return the new root
        return newRoot

    # Gets the height of the tree
    def get_height(self, root):
        if (root == None):
            return 0
        return 1 + max(self.get_height(root.left_child), self.get_height(root.right_child))

    # Gets the difference between the heights of the sides of the tree with a tolerance of 1:-1
    def get_balance(self, root):
        if (root == None):
            return 0
        return self.get_height(root.left_child) - self.get_height(root.right_child)

    # Returns if a node is black or not
    def is_node_nlack(self, Node):
        return (Node.is_node_nlack if Node != None else True)

    # Returns if a node is red or not
    def is_node_red(self, Node):
        return (not Node.is_node_nlack if Node != None else False)

    # Sets the node to black and returns an updated node
    def set_node_to_black(self, Node, black=True):
        if (Node != None and Node.value != None):
            Node.is_node_nlack = black
            self.recentItems.append(Node.value)
            return Node
        return

    # Sets the node to red and returns an updated node
    def set_node_to_red(self, Node, black=False):
        if (Node != None and Node.value != None):
            Node.is_node_nlack = black
            self.recentItems.append(Node.value)
            return Node
        return

    # swaps a node's colors
    def swap_node_color(self, Node1, Node2):
        # Store the color of both nodes
        if Node1 is not None:
            Node1_color = Node1.is_node_nlack
        else:
            Node1_color = True
        if Node2 is not None:
            black = Node2.is_node_nlack
        else:
            black = True

        # Set the color of both nodes to the stored values
        Node1 = self.set_node_to_black(Node1, black)
        Node2 = self.set_node_to_black(Node2, black=Node1_color)

        # Add the values of both nodes to the recentItems list
        self.recentItems.extend([Node1.value, Node2.value])

        # Return both nodes
        return Node1, Node2

    # Returns if a node is double black or not
    def is_node_double_black(self, Node):
        return (Node.is_node_nlack == 2 if Node != None else False)

    # sets a node to double black
    def set_node_to_double_black(self, thisNode):
        # Check if the given node is `None`
        if (Node == None):
            # Create a new node with value `None` and color `2` (double black)
            tempNode = Node(None, 2)
            return tempNode
        # Set the color of the given node to double black (2)
        thisNode.is_node_nlack = 2
        # Append the value of the given node to the `recentItems` list
        self.recentItems.append(Node.value)
        return thisNode

    # deletes the node with the specified value from the Red-Black tree
    def delete(self, value, root):
        if (root == None):
            return

        # Reset the recentItems list
        self.recentItems = []

        # Store the current root value
        valueAtual = root.value

        # Call the delete_node method to delete the node with the specified value
        root = self.delete_node(value, root)

        # If the root's value is None, delete the root and return
        if (root.value == None):
            del root
            return
        # If the root's value is equal to the current root value, check if it's black
        elif (root.value == valueAtual):
            if (root.is_node_nlack):
                # Remove the root's value from the recentItems list
                self.recentItems[:] = [
                    value for value in self.recentItems if value != root.value]
        # Set the root to black
        root.is_node_nlack = True

        # Move the first item in the recentItems list to the end
        self.recentItems.append(self.recentItems.pop(0))

        # Insert None at the beginning of the recentItems list
        self.recentItems.insert(0, None)

        return root

    def delete_node(self, value, root):
        if (root == None):  # value not found
            # Append None to the recentItems list
            self.recentItems.append(None)
            return root
        if (root.value == None):  # Node None double black
            return root
        if (value < root.value):  # Recursive to the left
            # Recursively call delete_node on the left child
            root.left_child = self.delete_node(value, root.left_child)
        elif (value > root.value):  # Recursive to the right
            # Recursively call delete_node on the right child
            root.right_child = self.delete_node(value, root.right_child)
        else:
            # localized value, but contains both branches
            if (root.left_child != None and root.right_child != None):
                # Find the largest sub-substitute on the left-hand branch
                substitute = self.find_largest_node(root.left_child)
                # Append the value of the found node to the recentItems list
                self.recentItems.append(substitute.value)
                # Swap the values of the current and substituted
                root.value = substitute.value
                # Recursive, on the left-hand branch, to delete the new Node containing the value of value
                root.left_child = self.delete_node(
                    substitute.value, root.left_child)
            else:  # value (re)located, with at least one branch None
                if (root.left_child == None):
                    # The surrogate will be a "valid" child, if any, else None
                    substitute = root.right_child
                else:
                    substitute = root.left_child
                if (substitute != None):
                    # Append the value of the found node to the recentItems list
                    self.recentItems.append(substitute.value)
                else:
                    # Append None to the recentItems list
                    self.recentItems.append(None)
                # If either the surrogate or current child is RED, just set the surrogate to BLACK.
                if (self.is_node_red(substitute) or self.is_node_red(substitute)):
                    substitute = self.set_node_to_black(substitute)
                else:
                    # Otherwise, the replacement becomes double black (even if it is None), and you will need to rebalance.
                    substitute = self.set_node_to_double_black(substitute)

                # delete the original node
                del root
                return substitute

        brother = None

        # Check if the double black node is on the left branch
        if (self.is_node_double_black(root.left_child)):
            brother = root.right_child
            cousin = True
        # Check if the double black node is on the right branch
        elif (self.is_node_double_black(root.right_child)):
            brother = root.left_child
            cousin = False

        # If there is a double black node, there will be a valid brother node
        if (brother != None):
            # If the brother node is BLACK
            if (brother.is_node_nlack):
                # If the double black node is on the left branch
                if (cousin):
                    # Undo the double black condition of the left branch
                    root.left_child = self.set_node_to_black(root.left_child)
                # If the double black node is on the right branch
                else:
                    # Undo the double black condition of the right branch
                    root.right_child = self.set_node_to_black(root.right_child)

                # If both nephew nodes are BLACK (or None)
                if (self.is_node_nlack(brother.left_child) and self.is_node_nlack(brother.right_child)):
                    # Color the brother node in RED
                    brother = self.set_node_to_red(brother)
                    # If the root node is BLACK, make it double black
                    if (self.is_node_nlack(root)):
                        root = self.set_node_to_double_black(root)
                    # If the root node is RED, make it BLACK (increase its black level by 1)
                    else:
                        root = self.set_node_to_black(root)
                # If at least one nephew node is RED
                else:
                    # If the brother node is on the right branch
                    if (cousin):
                        # Right-Left rotation if the right nephew node is BLACK
                        if (self.is_node_nlack(brother.right_child)):
                            brother = self.rotate_right(brother)
                            brother.right_child, brother = self.swap_node_color(
                                brother.right_child, brother)
                        # Update the right branch of the root node to be the brother node
                        root.right_child = brother
                        # Left rotation on the root node
                        root = self.rotate_left(root)
                        # Swap the colors of the root and left branches
                        root.left_child, root = self.swap_node_color(
                            root.left_child, root)
                        # Make the right branch BLACK (even if it is None)
                        root.right_child = self.set_node_to_black(
                            root.right_child, black=self.is_node_nlack(root.left_child))

                    else:  # brother on the left-hand branch
                        # Left - Right, if not Left - Left
                        if (self.is_node_nlack(brother.left_child)):
                            # Perform a left rotation on the brother
                            brother = self.rotate_left(brother)
                            # Swap colors of the brother and its left child
                            brother.left_child, brother = self.swap_node_color(
                                brother.left_child, brother)
                        # Set the left child of root to the modified brother
                        root.left_child = brother
                        # Perform a right rotation on the root
                        root = self.rotate_right(root)
                        # Swap colors of the root and its right child
                        root.right_child, root = self.swap_node_color(
                            root.right_child, root)
                        # Set the left child of root to black and maintain the same black level as the right child
                        root.left_child = self.set_node_to_black(
                            root.left_child, black=self.is_node_nlack(root.right_child))
            else:  # If the brother is RED
                if (cousin):  # If brother on the left-hand branch
                    # Perform a left rotation on the root
                    root = self.rotate_left(root)
                    # Swap colors of the root and its left child
                    root.left_child, root = self.swap_node_color(
                        root.left_child, root)
                    # Set the right child of root to black
                    root.right_child = self.set_node_to_black(root.right_child)
                    # Perform delete operation on the left child of root
                    root.left_child = self.delete_node(value, root.left_child)
                else:  # If brother in the Right branch
                    # Perform a right rotation on the root
                    root = self.rotate_right(root)
                    # Swap colors of the root and its right child
                    root.right_child, root = self.swap_node_color(
                        root.right_child, root)
                    # Set the left child of root to black
                    root.left_child = self.set_node_to_black(root.left_child)
                    # Perform delete operation on the right child of root
                    root.right_child = self.delete_node(
                        value, root.right_child)
        # Return the modified root
        return root

    # This function searches for a specific value in a red-black tree recursively.
    def search_for_value(self, value, root):
        if (root != None):
            if (value == root.value):
                return root
            elif (value < root.value):
                return self.search_for_value(value, root.left_child)
            else:
                return self.search_for_value(value, root.right_child)
        return

    # Returns the largest Node
    def find_largest_node(self, Node):
        if (Node.right_child != None):
            return self.find_largest_node(Node.right_child)
        return Node


class Visualization:

    def __init__(self, root):
        """
        Initializes the UI elements for the Red-Black Tree
        """
        # create a frame as the main container for UI elements
        self.frame = Frame(root)
        self.frame.pack()

        # create a label for the number entry
        self.label = Label(self.frame, text="Number:")
        self.label.pack(side=LEFT)

        # create an entry for inputting the number
        self.entry = Entry(self.frame, justify="center", width=7)
        self.entry.bind("<Return>", self.insert_tree)
        self.entry.pack(side=LEFT)

        # create an insert button
        self.insertButton = Button(
            self.frame, text="Insert", state="disabled", command=self.insert_tree)
        self.insertButton.pack(side=LEFT)

        # create a delete button
        self.deleteButton = Button(
            self.frame, text="delete", state="disabled", command=self.delete_node)
        self.deleteButton.pack(side=LEFT)

        # create a search button
        self.searchButton = Button(
            self.frame, text="Search", state="disabled", command=self.search_tree)
        self.searchButton.pack(side=LEFT)

        # create a run button
        self.runButton = Button(
            self.frame, text="Run", state="normal", command=self.insert_tree_animation)
        self.runButton.pack(side=LEFT)

        # create a checkbutton to toggle NIL nodes
        self.drawNIL = FALSE
        self.Checkbutton = Checkbutton(self.frame, state="normal", text='NIL Toggle',
                                       variable=self.drawNIL, onvalue=1, offvalue=0, command=self.toggle_nil)
        self.Checkbutton.pack(side=LEFT)

        # create a second frame
        self.secondFrame = Frame(root)
        self.secondFrame.pack()

        # create a message label
        self.message_label = Label(self.secondFrame, text="")
        self.message_label.pack(side=RIGHT)

        # create a canvas for displaying the tree
        self.canvas = Canvas(root, width=1400, height=768, bg='grey')
        self.canvas.pack()

        # initialize the size of the nodes
        self.size = 30
        self.RBT = RBT()
        self.root = None
        self.Trees = [None]
        self.Index = 0
        self.find = None
        self.draw_tree()
        self.message = ""

    def insert_tree_animation(self, *args):
        """
        Runs the animation for inserting nodes into the tree, updated after each insertion
        """
        # A list of hardcoded and shuffled numbers
        hardcoded_and_shuffled_list = [
            12, 5, 9, 4, 17, 3, 7, 20, 16, 19, 0, 6, 1, 10, 18, 15, 14, 2, 11, 8, 13]
        # numbers = list(range(0, 21))  # Create a list of numbers 0 to 20

        # Resetting the message label and disabling the run button
        self.message = ""
        self.runButton['state'] = 'disabled'
        self.Checkbutton['state'] = 'disabled'

        # Iterating over the list of numbers
        for value in hardcoded_and_shuffled_list:

            # If there is no root node, create one
            if self.root == None:
                self.message = "Creating the root..."
                self.message_label.config(text=self.message)

            # If there is already a root node, insert the new value
            else:
                self.message = "Inserting {} and Updating Tree...".format(
                    str(value))
                self.message_label.config(text=self.message)

            # Insert the new value into the binary tree
            self.root = self.RBT.insert(int(value), self.root)

            # If the value has already been inserted, set it as the value to be found
            if (self.RBT.recentItems[0] == None):
                self.find = int(value)
                self.message = "{} has already been inserted".format(
                    str(value))
                self.message_label.config(text=self.message)

            # Draw the updated tree and reset the find value to None
            self.draw_tree()
            self.find = None

            # Update the canvas and wait for one second
            self.canvas.update_idletasks()
            time.sleep(1)

        # Re-enable the insert, delete, and search buttons and reset the message label
        self.insertButton['state'] = 'normal'
        self.deleteButton['state'] = 'normal'
        self.searchButton['state'] = 'normal'
        self.message = ""
        self.message_label.config(text=self.message)

    def insert_tree(self, *args):
        """
        Insert a value into the binary tree and update the display of the tree
        """
        try:
            value = int(self.entry.get())
        except Exception:
            return

        # Clear display message
        self.message = ""
        self.message_label.config(text=self.message)
        self.entry.delete(0, 'end')

        if self.root == None:
            # Update display message
            self.message = "Creating the root..."
            self.message_label.config(text=self.message)

            # Enable delete and search buttons
            self.deleteButton['state'] = 'normal'
            self.searchButton['state'] = 'normal'
            self.runButton['state'] = 'normal'
        else:
            # Update display message
            self.message = "Inserting {} and Updating Tree...".format(
                str(value))
            self.message_label.config(text=self.message)

        # Insert value into binary tree
        self.root = self.RBT.insert(value, self.root)

        # Store the value that was recently added
        if (self.RBT.recentItems[0] == None):
            self.find = value

        # Update display of the binary tree
        self.draw_tree()

        # Reset find value
        self.find = None

    def delete_node(self, *args):
        """
        deletes node from tree
        """
        # Get value from entry widget
        try:
            value = int(self.entry.get())
        except Exception:
            return

        # Reset the message label
        self.message = ""
        self.message_label.config(text=self.message)
        self.entry.delete(0, 'end')

        # Notify user of deletion in progress
        self.message = "Deleting {}... ".format(str(value))
        self.message_label.config(text=self.message)

        # delete the node from the tree
        self.root = self.RBT.delete(value, self.root)

        # Check if tree is empty
        if (self.root == None):
            self.message = "the tree is empty"
            self.message_label.config(text=self.message)
            self.deleteButton['state'] = 'disabled'
            self.searchButton['state'] = 'disabled'

        # Redraw the tree
        self.draw_tree()

    def search_tree(self, *args):
        """
        Searches the tree for a value and reports if it is found
        """
        # Retrieve the value from the entry widget
        try:
            value = int(self.entry.get())
        except Exception:
            # Return if value cannot be converted to an integer
            return

        # Reset the message label text and update it to indicate the search is in progress
        self.message = ""
        self.message_label.config(text=self.message)
        self.message = "Searching for {}...".format(str(value))
        self.message_label.config(text=self.message)

        # Call the `search_for_value` method of the `RBT` class to find the node
        Node = self.RBT.search_for_value(value, self.root)

        # Check if the node was found or not
        if (Node == None):
            self.message = "{} was not found".format(str(value))
            self.message_label.config(text=self.message)
        else:
            self.message = "{} was found".format(str(value))
            self.message_label.config(text=self.message)
            self.find = value
            self.draw_tree()
            self.find = None

    def draw_tree(self):
        """
        Draws the red-black tree on the canvas widget.
        """
        # Clear the canvas
        self.canvas.delete(ALL)

        # Check if the root of the binary tree exists
        if (self.root != None):
            # Set the maximum width of the canvas to the width of the window minus a margin of 40
            self.xmax = self.canvas.winfo_width() - 40

            # Set the maximum height of the canvas to the height of the window
            self.ymax = self.canvas.winfo_height()

            # Get the number of lines required to display the binary tree
            self.numberLines = self.RBT.get_height(self.root)

            # Calculate the x-coordinate of the root node
            Xcoordinate = int(self.xmax / 2)

            # Calculate the y-coordinate of the root node
            Ycoordinate = int(self.ymax / (self.numberLines + 2))

            # Draw the binary tree starting from the root node
            self.draw_node(self.root, Xcoordinate, Ycoordinate, 1)

    def draw_node(self, Node, posX, posY, line):
        """
        Draws a node of the red-black tree.
        """
        # Reset the message text
        self.message = ""

        # Calculate the vertical space between lines
        y = self.ymax / (self.numberLines + 1)
        # Calculate the number of columns in the current line
        numberColumns = 2 ** (line + 1)
        # Calculate the horizontal space between nodes
        x = self.xmax / numberColumns
        # Calculate the position of the child node on the Y axis
        childPositionY = posY + y

        # Draw the right child node, if it exists
        if (Node.right_child != None):
            childPositionX = posX + (x + 4)
            # Draw a line connecting the current node to its right child
            self.canvas.create_line(posX, posY, childPositionX,
                                    childPositionY, fill="white")
            # Draw the right child node
            self.draw_node(Node.right_child, childPositionX,
                           childPositionY, line + 1)
        else:
            # If NIL nodes should be drawn, draw a line to the right NIL node
            if (self.drawNIL == TRUE):
                childPositionX = posX + (x + 4)
                self.canvas.create_line(
                    posX, posY, childPositionX, childPositionY, fill="white")
                self.draw_right_nil(posX, posY, line)

        # Draw the left child node, if it exists
        if (Node.left_child != None):
            childPositionX = posX - (x + 4)
            # Draw a line connecting the current node to its left child
            self.canvas.create_line(posX, posY, childPositionX,
                                    childPositionY, fill="white")
            # Draw the left child node
            self.draw_node(Node.left_child, childPositionX,
                           childPositionY, line + 1)
        else:
            # If NIL nodes should be drawn, draw a line to the left NIL node
            if (self.drawNIL == TRUE):
                childPositionX = posX - (x + 4)
                self.canvas.create_line(
                    posX, posY, childPositionX, childPositionY, fill="white")
                self.draw_left_nil(posX, posY, line)

        # Calculate the coordinates of the current node's oval
        Xcoordinate = int(posX - self.size / 2)
        Ycoordinate = int(posY - self.size / 2)
        Xcoordinate2 = int(posX + self.size / 2)
        Ycoordinate2 = int(posY + self.size / 2)

        # Highlight recently updated node
        if (Node.value in self.RBT.recentItems[1: -1]):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='paleturquoise')

        # Highlight the most recently inserted node
        if (Node.value == self.RBT.recentItems[0]):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='lightgreen')

        # Color the node differently if it was found
        elif (Node.value == self.find):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='pink')
            self.message = "{} was found".format(str(Node.value))
            self.message_label.config(text=self.message)

        # Color the node differently depending on its status of red of black
        NodeColor = ("black" if self.RBT.is_node_nlack(Node) else "red")
        self.canvas.create_oval(Xcoordinate, Ycoordinate,
                                Xcoordinate2, Ycoordinate2, fill=NodeColor)
        self.canvas.create_text(posX, posY, text=str(Node.value), fill="white")

    def draw_right_nil(self, posX, posY, line):
        # Calculate y-coordinate for child node
        y = self.ymax / (self.numberLines + 1)

        # Calculate number of columns for current line
        numberColumns = 2 ** (line + 1)

        # Calculate x-coordinate for child node
        x = self.xmax / numberColumns

        # Calculate position for child node
        childPositionY = posY + y
        childPositionX = posX + (x + 4)

        # Calculate coordinates for node rectangle
        Xcoordinate = int(childPositionX - self.size / 4)
        Ycoordinate = int(childPositionY - self.size / 4)
        Xcoordinate2 = int(childPositionX + self.size / 4)
        Ycoordinate2 = int(childPositionY + self.size / 4)

        # Draw the NIL node rectangle
        self.canvas.create_rectangle(
            Xcoordinate, Ycoordinate, Xcoordinate2, Ycoordinate2, fill="black")

        # Add the text "NIL" to the node rectangle
        self.canvas.create_text(
            childPositionX + 1, childPositionY, text="NIL", fill="white", font=('Times', 6))

    def draw_left_nil(self, posX, posY, line):
        # Calculate y-coordinate for child node
        y = self.ymax / (self.numberLines + 1)

        # Calculate number of columns for current line
        numberColumns = 2 ** (line + 1)

        # Calculate x-coordinate for child node
        x = self.xmax / numberColumns

        # Calculate position for child node
        childPositionY = posY + y
        childPositionX = posX - (x + 4)

        # Calculate coordinates for node rectangle
        Xcoordinate = int(childPositionX - self.size / 4)
        Ycoordinate = int(childPositionY - self.size / 4)
        Xcoordinate2 = int(childPositionX + self.size / 4)
        Ycoordinate2 = int(childPositionY + self.size / 4)

        # Draw the NIL node rectangle
        self.canvas.create_rectangle(
            Xcoordinate, Ycoordinate, Xcoordinate2, Ycoordinate2, fill="black")

        # Add the text "NIL" to the node rectangle
        self.canvas.create_text(
            childPositionX + 1, childPositionY, text="NIL", fill="white", font=('Times', 6))

    def toggle_nil(self):
        # Toggles the `drawNIL` attribute between True and False, changing whether NIL is drawn or not.
        if self.drawNIL:
            self.drawNIL = False
        else:
            self.drawNIL = True


# main execution
if __name__ == '__main__':
    root = Tk(None, None, " Red - Black Tree")
    root.geometry("1024x750")
    RBT_visualization = Visualization(root)
    root.mainloop()
