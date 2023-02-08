import time

import tkinter as tk

import fibonacci_heap

# Display each node of the fibonacci heap
def display(canvas: tk.Canvas,
            current_node: fibonacci_heap.Node,
            min_node: fibonacci_heap.Node, 
            x: int,
            y: int,) -> int:

    # Draw node
    if current_node.mark == True:
        canvas.create_oval(x, y, x+30, y+30, fill="red")
    else:
        canvas.create_oval(x, y, x+30, y+30, fill="white")
    canvas.create_text(x+15, y+15, text=current_node.key)

    # Draw each linked node.
    current_child = current_node.child
    offset = -30 * (2**(current_node.degree-2)) * (current_node.degree-1) / 2
    for child in range(current_node.degree):

        # Draw Parent Links
        canvas.create_line(x+15, y+30, x+offset+15, y+100)
        canvas.pack()

        # Draw Child Links
        display(canvas, current_child, min_node, x+offset, y+100)

        # Draw Sibling Links
        if current_child != current_node.child.left:
            # Draw right line
            offset2 = offset + 60 + (2**child * 30)
            canvas.create_line(x+30+offset, y+115, x+offset2, y+115)
            offset = offset2
            canvas.pack()

        # Iterate child.
        current_child = current_child.right
    
    if current_node.parent == None and current_node.right != min_node:
        canvas.create_line(x+30, y+15, x+500, y+15)
        display(canvas, current_node.right, min_node, x+500, y)

def main() -> None:
    window = tk.Tk()
    window.geometry("1600x1200")
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.create_text(300, 50, text="Yo")
    canvas.pack()
    FH = fibonacci_heap.FibonacciHeap()
    for i in range(26):
        FH.insert(i)
        if i % 5 == 1:
            FH.extract_min()
        time.sleep(1)
        canvas.delete('all')
        display(canvas, FH.min, FH.min, 181, 100)
    # x = FH.search(18)
    # FH.delete(x)
    # display(canvas, FH.min, FH.min, 181, 100)
    window.mainloop()
    # window.attributes('-fullscreen',True)

if __name__ == '__main__':
    main()