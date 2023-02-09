import time
import threading
from tkinter.ttk import Label
import tkinter as tk

import fibonacci_heap

# Display each node of the fibonacci heap
def display(current_node: fibonacci_heap.Node,
            min_node: fibonacci_heap.Node, 
            x: int,
            y: int,) -> int:
    canvas.configure(background='grey')
    text = Label(canvas, text="Fibonnaci Heap")
    text.place(x=350,y=50)

    # Draw node
    if current_node.mark == True:
        canvas.create_oval(x, y, x+30, y+30, fill="blue")
    else:
        canvas.create_oval(x, y, x+30, y+30, fill="red")
    canvas.create_text(x+15, y+15, text=current_node.key)

    # Draw each linked node.
    current_child = current_node.child
    offset = -30 * (2**(current_node.degree-2)) * (current_node.degree-1) / 2
    for child in range(current_node.degree):

        # Draw Parent Links
        canvas.create_line(x+15, y+30, x+offset+15, y+100, arrow=tk.LAST)

        # Draw Child Links
        display(current_child, min_node, x+offset, y+100)

        # Draw Sibling Links
        if current_child != current_node.child.left:
            # Draw right line
            offset2 = offset + 60 + (2**child * 30)
            canvas.create_line(x+30+offset, y+115, x+offset2, y+115, arrow=tk.BOTH)
            offset = offset2

        # Iterate child.
        current_child = current_child.right
    
    if current_node.parent == None and current_node.right != min_node:
        canvas.create_line(x+30, y+15, x+240, y+15, arrow=tk.BOTH)
        display(current_node.right, min_node, x+240, y)

def run_heap():
    FH = fibonacci_heap.FibonacciHeap()
    for i in range(26):
        FH.insert(i)
        if i % 5 == 1:
            FH.extract_min()
        time.sleep(1)
        canvas.delete('all')
        display(FH.min, FH.min, 181, 100)
    # x = FH.search(18)
    # FH.delete(x)
    # display(FH.min, FH.min, 181, 100)
    # window.attributes('-fullscreen',True)

# Create Window
window = tk.Tk()
window.geometry("1800x1200")
# Create button
UI_frame = tk.Frame(window, width= 1800, height=600)
UI_frame.grid(row=0, column=0, padx=10, pady=5)
b1 = tk.Button(UI_frame, text="Run", command=threading.Thread(target=run_heap).start)
b1.grid(row=0, column=0, padx=5, pady=5)
canvas = tk.Canvas(window, width=1600, height=1200)
canvas.grid(row=1, column=0)
window.mainloop()