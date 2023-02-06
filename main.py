import tkinter as tk

import fibonacci_heap

# # Create a Fibonacci Tree
# FH = fibonacci_heap.FibonacciHeap()
# FH.insert(102)
# FH.insert(11)
# FH.insert(10)
# FH.insert(12)
# print(f'Min before decrease {FH.min.key}')
# FH.decrease_key(FH.search(11), 7)
# print(f'Min after decrease {FH.min.key}')
# print(f'num_nodes: {FH.num_nodes}')
# print(f'num_trees: {FH.num_trees}')


# # Union Test
# FH2 = fibonacci_heap.FibonacciHeap()
# FH2.insert(300)
# FH2.insert(110)
# FH2.insert(9)
# FH2.insert(6)

# FH.union(FH2)
# # print(f'New min key: {FH.min.key}')

# # print(f'num_nodes before: {FH.num_nodes}')
# # print(f'num_trees before: {FH.num_trees}\n')


# old_min = FH.extract_min()
# print(f'Extracted: {old_min.key}')
# print(f'num_nodes after: {FH.num_nodes}')
# print(f'num_trees after: {FH.num_trees}')
# print(f'new_min degree: {FH.min.degree}')
# print(f'new_min key: {FH.min.key}')

# print(FH.min.key)
# print(FH.min.child.key)
# print(FH.min.child.right.key) #
# print(FH.min.right.key)
# print(FH.min.right.child.key)
# print(FH.min.right.right.key)


FH = fibonacci_heap.FibonacciHeap()
for i in range(20):
    FH.insert(i)


old_min = FH.extract_min()
print(f'Extracted: {old_min.key}')
print(FH.min.key)
print(f'num_nodes after: {FH.num_nodes}')
print(f'num_trees after: {FH.num_trees}')
print(f'new_min degree: {FH.min.degree}')
print(f'new_min key: {FH.min.key}')




# Display Each Node of the fibonacci heap
def display(canvas, current_node, x, y, current_tree=None, current_root=None):

    # If display was called, set current tree and node.
    if current_node == FH.min:
        current_tree = FH.min
        current_root = FH.min
        print(type(x))

    # Draw node
    canvas.create_oval(x, y, x+30, y+30, fill="white")
    canvas.create_text(x+15, y+15, text=current_node.key)

    # for node in range(current_node.degree):
    #     display()

    if current_node.child != None:
        # Draw link
        canvas.create_line(x+15, y+30, x+15, y+100)
        canvas.pack()
        # Change y position
        y += 100
        current_node = current_node.child
        current_root = current_node
        display(canvas, current_node, x, y, current_tree, current_root)
    elif current_node.right != current_root:
        # Draw link
        canvas.create_line(x+30, y+15, x+100, y+15)
        canvas.pack()
        # Change x position
        x += 100
        # Change_position(x+5, y)
        display(canvas, current_node.right, x, y, current_tree, current_root)
    elif current_tree.right != FH.min:
        # Draw link
        y = 10
        canvas.pack()
        # Change position
        current_tree = current_tree.right
        current_node = current_tree
        current_root = FH.min
        display(canvas, current_node, x, y, current_tree, current_root)

# window = tk.Tk()
# greeting = tk.Label(text="Hello, Tkinter")
# greeting.pack()
# window.mainloop()

root = tk.Tk()
root.geometry("800x600")
# root.attributes('-fullscreen',True)
canvas = tk.Canvas(root, width=800, height=600)
canvas.create_text(300, 50, text="HELLO WORLD", fill="black", font=('Helvetica 15 bold'))
canvas.pack()

display(canvas, FH.min, 10, 10, 0)

root.mainloop()