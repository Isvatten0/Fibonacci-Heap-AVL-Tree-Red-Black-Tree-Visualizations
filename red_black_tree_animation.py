# Created by the Balanced Fibs:

from tkinter import *
import time

highlight = 3


class Node:
    def __init__(self, value, black, left=None, right=None):
        self.value = value
        self.isNodeblack = black
        self.left = left
        self.right = right


class BinaryTree:
    # recentItems are the Nodes changed / created in the last insertion or removal.
    # The first element is the principal,
    # because it is either the inserted Node or the replacement for the removed one.
    def __init__(self, root=None):
        self.root = root
        if (root != None):
            self.recentItems = [root.value, None]
        else:
            self.recentItems = [None]
    # Node Node

    def createNode(self, value, black):
        return Node(value, black)

    # Calculate the height of black nodes only,
    # which must be constant for the left and right branches of a red-black tree.

    def getLevel(self, root):
        if (root == None):
            return 1, 1
        altBlackleft, altRedleft = self.getLevel(root.left)
        altBlackRight, altRedRight = self.getLevel(root.right)
        return root.isNodeblack + max(altBlackleft, altBlackRight), not root.isNodeblack + max(altRedleft, altRedRight)

    def getHeight(self, root):
        if (root == None):
            return 0
        return 1 + max(self.getHeight(root.left), self.getHeight(root.right))
    # Calculates the total balance, which doesn't need to be as accurate as the AVL.

    def getBalance(self, root):
        if (root == None):
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
    # Rotate Right

    def rotateRight(self, oldRoot):
        newRoot = oldRoot.left
        oldRoot.left, newRoot.right = newRoot.right, oldRoot
        if (oldRoot.value == self.recentItems[0]):
            self.recentItems[0] = newRoot.value
        self.recentItems.extend([oldRoot.value, newRoot.value, oldRoot.left])
        return newRoot
        # Rotate left

    def rotateleft(self, oldRoot):
        newRoot = oldRoot.right
        oldRoot.right, newRoot.left = newRoot.left, oldRoot
        if (oldRoot.value == self.recentItems[0]):
            self.recentItems[0] = newRoot.value
        self.recentItems.extend([oldRoot.value, newRoot.value, oldRoot.right])
        return newRoot

    # True if the Node is black or None, else false
    # "None" nodes are always black

    def isNodeBlack(self, Node):
        return (Node.isNodeblack if Node != None else True)
    # True if the Node is red, otherwise false

    def isNodeRed(self, Node):
        return (not Node.isNodeblack if Node != None else False)
    # Returns the Node with the modified black attribute (default: True, or Black)

    def setNodeToBlack(self, Node, black=True):
        if (Node != None and Node.value != None):
            Node.isNodeblack = black
            self.recentItems.append(Node.value)
            return Node
        return
    # Returns the Node with the modified black attribute (default: False, or Red)

    def setNodeToRed(self, Node, black=False):
        if (Node != None and Node.value != None):
            Node.isNodeblack = black
            self.recentItems.append(Node.value)
            return Node
        return

    # Returns the two input Nodes, with their black attributes swapped

    def swapNodeColor(self, Node1, Node2):
        if Node1 is not None:
            Node1_blackness = Node1.isNodeblack
        else:
            Node1_blackness = True
        # Node1_blackness = self.isNodeBlack(Node1)
        if Node2 is not None:
            black = Node2.isNodeblack
        else:
            black = True
        Node1 = self.setNodeToBlack(Node1, black)
        Node2 = self.setNodeToBlack(Node2, black = Node1_blackness)
        self.recentItems.extend([Node1.value, Node2.value])
        return Node1, Node2
    # Initialize the insert recursion
    # Root is always BLACK.

    def insert(self, value, root):
        root, case = self.insertNode(value, root)
        root.isNodeblack = True
        self.recentItems.append(None)
        return root
    # Common recursive binary insertion, added balancing for red-black tree
    # About the "case" variable:
    # If 0 means no more modifications needed
    # If 1 means that the current Node(root) is the father of the inserted Node
    # If 2 means that the current Node (root) is the grandfather of the entered Node

    def insertNode(self, value, root):
        # The value does not exist, so a corresponding Node is created. Always RED.
        if (root == None):
            Node = self.createNode(value, False)
            self.recentItems = [value]
            return Node, 1
        if (value < root.value):  # Recursive for the left branch
            root.left, case = self.insertNode(value, root.left)
            uncle = root.right
        elif (value > root.value):  # Recursive for the right branch
            root.right, case = self.insertNode(value, root.right)
            uncle = root.left
        else:  # repeated value, so case = 0
            self.recentItems = []
            return root, 0

        if (case == 1):
            # If father is black, you don't need to modify anything else.
            if (root.isNodeblack):
                case = 0
            else:  # If not, it will depend on the uncle, so one must return to the grandfather.
                case = 2
        elif (case == 2):
            if (self.isNodeBlack(uncle)):  # If the uncle is black, the operation is similar to the AVL tree
                Balance = self.getBalance(root)
                if (Balance > 1):  # Unbalanced to left
                    if (value > root.left.value):  # Left - Right, if not Left - Left
                        root.left = self.rotateleft(root.left)
                    root = self.rotateRight(root)
                    # The difference to the AVL is in this color change between root and uncle
                    root.right, root = self.swapNodeColor(root.right, root)
                    case = 0  # At the end, no further modifications are needed
                elif (Balance < - 1):  # Right Unbalanced
                    if (value < root.right.value):  # Right - Left, if not Right - Right
                        root.right = self.rotateRight(root.right)
                    root = self.rotateleft(root)
                    # The difference to the AVL is in this color change between root and uncle
                    root.left, root = self.swapNodeColor(root.left, root)
                    case = 0  # At the end, no further modifications are needed
            else:  # If the uncle is red, paint the father and uncle black, the grandfather red, and consider the grandfather the new son
                root.left = self.setNodeToBlack(root.left)
                root.right = self.setNodeToBlack(root.right)
                root = self.setNodeToRed(root)
                case = 1  # Grandfather (current node) becomes a son.
        return root, case
    # Returns the Node with attribute black = 2
    # It is a special Node to be used temporarily in the removal process

    def setNodeToDoubleBlack(self, Node):
        if (Node == None):
            return self.createNode(None, 2)
        Node.isNodeblack = 2
        self.recentItems.append(Node.value)
        return Node
    # Test if the Node is "double black", or black = 2

    def isNodeDoubleBlack(self, Node):
        return (Node.isNodeblack == 2 if Node != None else False)
    # Returns the largest Node on the left-left branch

    def findRightNode(self, Node):
        if (Node.right != None):
            return self.findRightNode(Node.right)
        return Node
    # Initialize the remove recursion
    # Root is always BLACK

    def Delete(self, value, root):
        if (root == None):
            return
        self.recentItems = []
        valueAtual = root.value
        root = self.DeleteNode(value, root)
        if (root.value == None):
            del root
            return
        elif (root.value == valueAtual):
            if (root.isNodeblack):
                self.recentItems[:] = [
                    value for value in self.recentItems if value != root.value]
        root.isNodeblack = True
        self.recentItems.append(self.recentItems.pop(0))
        self.recentItems.insert(0, None)
        return root
    # Common binary removal, added balance repair for red-black tree
    # At some point it is necessary to consider None as being a Node None with black = 2,
    # that is, a double black None, however it is soon replaced by None.

    def DeleteNode(self, value, root):
        if (root == None):  # value not found
            self.recentItems.append(None)
            return root
        if (root.value == None):  # Node None double black
            return root
        if (value < root.value):  # Recursive to the left
            root.left = self.DeleteNode(value, root.left)
        elif (value > root.value):  # Recursive to the right
            root.right = self.DeleteNode(value, root.right)
        else:
            # localized value, but contains both branches
            if (root.left != None and root.right != None):
                # Find the largest sub-substitute on the left-hand branch
                subs = self.findRightNode(root.left)
                self.recentItems.append(subs.value)
                root.value = subs.value  # Swap the values ​​of the current and substituted
                # Recursive, on the left-hand branch, to Delete the new Node containing the value of value
                root.left = self.DeleteNode(subs.value, root.left)
            else:  # value (re)located, with at least one branch None
                if (root.left == None):
                    subs = root.right  # The surrogate will be a "valid" child, if any, else None
                else:
                    subs = root.left
                if (subs != None):
                    self.recentItems.append(subs.value)
                else:
                    self.recentItems.append(None)
                # If either the surrogate or current child is RED, just set the surrogate to BLACK.
                if (self.isNodeRed(root) or self.isNodeRed(subs)):
                    subs = self.setNodeToBlack(subs)
                else:
                    # Otherwise, the replacement becomes double black (even if it is None), and you will need to rebalance.
                    subs = self.setNodeToDoubleBlack(subs)

                del root
                return subs
        # if (root != None):
        # rebalance
        # First identify the sibling and its branch
        brother = None
        if (self.isNodeDoubleBlack(root.left)):
            brother = root.right
            cousin = True
        elif (self.isNodeDoubleBlack(root.right)):
            brother = root.left
            cousin = False
        # If there is a double black, there will be a valid brother.
        if (brother != None):
            if (brother.isNodeblack):  # If the brother is BLACK
                if (cousin):
                    # Undo the substitute's double black condition
                    root.left = self.setNodeToBlack(root.left)
                else:
                    root.right = self.setNodeToBlack(root.right)
                # If the nephews are both BLACK (or None)
                if (self.isNodeBlack(brother.left) and self.isNodeBlack(brother.right)):
                    # brother is colored in RED
                    brother = self.setNodeToRed(brother)
                    if (self.isNodeBlack(root)):
                        # father becomes double black if it is black
                        root = self.setNodeToDoubleBlack(root)
                    else:
                        # Or black if RED (i.e. black level is increased by 1)
                        root = self.setNodeToBlack(root)
                else:  # If at least one nephew is red
                    if (cousin):  # brother in Right branch
                        if (self.isNodeBlack(brother.right)):  # Right - Left, if not Right - Right
                            brother = self.rotateRight(brother)
                            brother.right, brother = self.swapNodeColor(
                                brother.right, brother)
                        root.right = brother
                        root = self.rotateleft(root)
                        root.left, root = self.swapNodeColor(root.left, root)
                        root.right = self.setNodeToBlack(
                            root.right, black=self.isNodeBlack(root.left))
                    else:  # brother on the left-hand branch
                        if (self.isNodeBlack(brother.left)):  # Left - Right, if not Left - Left
                            brother = self.rotateleft(brother)
                            brother.left, brother = self.swapNodeColor(
                                brother.left, brother)
                        root.left = brother
                        root = self.rotateRight(root)
                        root.right, root = self.swapNodeColor(root.right, root)
                        root.left = self.setNodeToBlack(
                            root.left, black=self.isNodeBlack(root.right))
            # If the brother is RED, some Color rotation and swap operations are performed,
            # to stop again if visiting the surrogate Node branch
            # Note that the Node double - black has not been undone yet.
            else:
                if (cousin):  # If brother on the left-hand branch
                    root = self.rotateleft(root)
                    root.left, root = self.swapNodeColor(root.left, root)
                    root.right = self.setNodeToBlack(root.right)
                    root.left = self.DeleteNode(value, root.left)
                else:  # If brother in the Right branch
                    root = self.rotateRight(root)
                    root.right, root = self.swapNodeColor(root.right, root)
                    root.left = self.setNodeToBlack(root.left)
                    root.right = self.DeleteNode(value, root.right)
        return root

    def searchForValue(self, value, root):
        if (root != None):
            if (value == root.value):
                return root
            elif (value < root.value):
                return self.searchForValue(value, root.left)
            else:
                return self.searchForValue(value, root.right)
        return


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
        self.entry.bind("<Return>", self.insertTree)
        self.entry.pack(side=LEFT)

        # create an insert button
        self.insertButton = Button(
            self.frame, text="Insert", state="disabled", command=self.insertTree)
        self.insertButton.pack(side=LEFT)

        # create a delete button
        self.deleteButton = Button(
            self.frame, text="Delete", state="disabled", command=self.deleteNode)
        self.deleteButton.pack(side=LEFT)

        # create a search button
        self.searchButton = Button(
            self.frame, text="Search", state="disabled", command=self.searchTree)
        self.searchButton.pack(side=LEFT)

        # create a run button
        self.runButton = Button(
            self.frame, text="Run", state="normal", command=self.insertTreeAnimation)
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
        self.BinaryTree = BinaryTree()
        self.root = None
        self.Trees = [None]
        self.Index = 0
        self.find = None
        self.drawTree()
        self.message = ""

    def insertTreeAnimation(self, *args):
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
            self.root = self.BinaryTree.insert(int(value), self.root)

            # If the value has already been inserted, set it as the value to be found
            if (self.BinaryTree.recentItems[0] == None):
                self.find = int(value)
                self.message = "{} has already been inserted".format(
                    str(value))
                self.message_label.config(text=self.message)

            # Draw the updated tree and reset the find value to None
            self.drawTree()
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

    def insertTree(self, *args):
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
        self.root = self.BinaryTree.insert(value, self.root)

        # Store the value that was recently added
        if (self.BinaryTree.recentItems[0] == None):
            self.find = value

        # Update display of the binary tree
        self.drawTree()

        # Reset find value
        self.find = None

    def deleteNode(self, *args):
        """
        Deletes node from tree
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

        # Delete the node from the tree
        self.root = self.BinaryTree.Delete(value, self.root)

        # Check if tree is empty
        if (self.root == None):
            self.message = "the tree is empty"
            self.message_label.config(text=self.message)
            self.deleteButton['state'] = 'disabled'
            self.searchButton['state'] = 'disabled'

        # Redraw the tree
        self.drawTree()

    def searchTree(self, *args):
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

        # Call the `searchForValue` method of the `BinaryTree` class to find the node
        Node = self.BinaryTree.searchForValue(value, self.root)

        # Check if the node was found or not
        if (Node == None):
            self.message = "{} was not found".format(str(value))
            self.message_label.config(text=self.message)
        else:
            self.message = "{} was found".format(str(value))
            self.message_label.config(text=self.message)
            self.find = value
            self.drawTree()
            self.find = None

    def drawTree(self):
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
            self.numberLines = self.BinaryTree.getHeight(self.root)

            # Calculate the x-coordinate of the root node
            Xcoordinate = int(self.xmax / 2)

            # Calculate the y-coordinate of the root node
            Ycoordinate = int(self.ymax / (self.numberLines + 2))

            # Draw the binary tree starting from the root node
            self.drawNode(self.root, Xcoordinate, Ycoordinate, 1)

    def drawNode(self, Node, posX, posY, line):
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
        if (Node.right != None):
            childPositionX = posX + (x + 4)
            # Draw a line connecting the current node to its right child
            self.canvas.create_line(posX, posY, childPositionX,
                                    childPositionY, fill="white")
            # Draw the right child node
            self.drawNode(Node.right, childPositionX, childPositionY, line + 1)
        else:
            # If NIL nodes should be drawn, draw a line to the right NIL node
            if (self.drawNIL == TRUE):
                childPositionX = posX + (x + 4)
                self.canvas.create_line(
                    posX, posY, childPositionX, childPositionY, fill="white")
                self.drawRightNIL(posX, posY, line)

        # Draw the left child node, if it exists
        if (Node.left != None):
            childPositionX = posX - (x + 4)
            # Draw a line connecting the current node to its left child
            self.canvas.create_line(posX, posY, childPositionX,
                                    childPositionY, fill="white")
            # Draw the left child node
            self.drawNode(Node.left, childPositionX, childPositionY, line + 1)
        else:
            # If NIL nodes should be drawn, draw a line to the left NIL node
            if (self.drawNIL == TRUE):
                childPositionX = posX - (x + 4)
                self.canvas.create_line(
                    posX, posY, childPositionX, childPositionY, fill="white")
                self.drawLeftNIL(posX, posY, line)

        # Calculate the coordinates of the current node's oval
        Xcoordinate = int(posX - self.size / 2)
        Ycoordinate = int(posY - self.size / 2)
        Xcoordinate2 = int(posX + self.size / 2)
        Ycoordinate2 = int(posY + self.size / 2)

        # Highlight recently updated node
        if (Node.value in self.BinaryTree.recentItems[1: -1]):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='paleturquoise')

        # Highlight the most recently inserted node
        if (Node.value == self.BinaryTree.recentItems[0]):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='lightgreen')

        # Color the node differently if it was found
        elif (Node.value == self.find):
            self.canvas.create_oval(Xcoordinate - highlight, Ycoordinate - highlight,
                                    Xcoordinate2 + highlight, Ycoordinate2 + highlight, fill='pink')
            self.message = "{} was found".format(str(Node.value))
            self.message_label.config(text=self.message)

        # Color the node differently depending on its status of red of black
        NodeColor = ("black" if self.BinaryTree.isNodeBlack(Node) else "red")
        self.canvas.create_oval(Xcoordinate, Ycoordinate,
                                Xcoordinate2, Ycoordinate2, fill=NodeColor)
        self.canvas.create_text(posX, posY, text=str(Node.value), fill="white")

    def drawRightNIL(self, posX, posY, line):
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

    def drawLeftNIL(self, posX, posY, line):
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
