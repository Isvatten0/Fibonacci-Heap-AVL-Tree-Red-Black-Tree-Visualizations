import tkinter as tk

class AVL:
    def __init__(self, root):
        self.window = root
        self.treeCanvasWidth = 1920
        self.treeCanvasHeight = 880

        #Build Main Containers
        self.treeCanvas = tk.Canvas(self.window,width=self.treeCanvasWidth,height=self.treeCanvasHeight,bg="white",relief=tk.RAISED,bd=8)
        self.UI = tk.Frame(self.window,width=400,height=200,bg="blue")
        
        #Place Main Containers
        self.treeCanvas.place(x=0,y=200)
        self.UI.place(x=self.treeCanvasWidth - 400,y=0)
        

        self.treePositions = [] #Possible positions in the tree
        self.tree = [] #Nodes currently in the tree
        self.nodeSize = 25 #Diameter of a node

        self.definepositions()

        #Place Secondary Items
        
        for pos in self.treePositions:
            self.treeCanvas.create_oval(self.getnodecoord(pos), fill="brown")

        self.treeCanvas.create_line(self.treePositions[0], self.treePositions[1], width = 5, fill = "black")
        
        

    def definepositions(self):
        for i in range(1, 7):
            for x in range(1, pow(2, i - 1) + 1):
                self.treePositions.append(((x*2 - 1)*self.treeCanvasWidth/(pow(2, i)), i*self.treeCanvasHeight/6 - 100))
        
    def getnodecoord(self, position):
        return (position[0] - self.nodeSize/2, position[1] - self.nodeSize/2, position[0] + self.nodeSize/2, position[1] + self.nodeSize/2)

    def parentposition(self, posIndex):
        return int((posIndex - 1)/2)
    def lchildposition(self, posIndex):
        return int(posIndex * 2 + 1)
    def rchildposition(self, posIndex):
        return int(posIndex * 2 + 2)
if __name__ == "__main__":
    window = tk.Tk()
    window.title("AVL Tree Visualization")
    window.geometry("1920x1080")
    window.maxsize(1920,1080)
    window.minsize(1920,1080)
    window.config(bg="grey")
    AVL(window)
    window.mainloop()
