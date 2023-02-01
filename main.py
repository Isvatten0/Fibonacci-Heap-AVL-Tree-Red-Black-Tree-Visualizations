import fibonacci_heap
# from matplotlib import pyplot

# Create a Fibonacci Tree
FH = fibonacci_heap.FibonacciHeap()
FH.insert(102)
FH.insert(11)
FH.insert(10)
FH.insert(12)
print(f'Min before decrease {FH.min.key}')
FH.decrease_key(FH.search(11), 7)
print(f'Min after decrease {FH.min.key}')
print(f'num_nodes: {FH.num_nodes}')
print(f'num_trees: {FH.num_trees}')


# Union Test
FH2 = fibonacci_heap.FibonacciHeap()
FH2.insert(300)
FH2.insert(110)
FH2.insert(9)
FH2.insert(6)

FH.union(FH2)
# print(f'New min key: {FH.min.key}')

# print(f'num_nodes before: {FH.num_nodes}')
# print(f'num_trees before: {FH.num_trees}\n')


old_min = FH.extract_min()
print(f'Extracted: {old_min.key}')
print(f'num_nodes after: {FH.num_nodes}')
print(f'num_trees after: {FH.num_trees}')
print(f'new_min degree: {FH.min.degree}')
print(f'new_min key: {FH.min.key}')

print(FH.min.key)
print(FH.min.child.key)
print(FH.min.child.right.key) #
print(FH.min.right.key)
print(FH.min.right.child.key)
print(FH.min.right.right.key)