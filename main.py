import fibbonacci_heap
from matplotlib import pyplot

# Create a Fibonacci Tree
FH = fibbonacci_heap.FibonacciHeap()
FH.insert(102)
FH.insert(11)
FH.insert(10)
FH.insert(7)
print(f'Min before decrease {FH.min.key}')
FH.decreaseKey(FH.search(11), 2)
print(f'Min after decrease {FH.min.key}')


# Union Test
FH2 = fibbonacci_heap.FibonacciHeap()
FH2.insert(300)
FH2.insert(110)
FH2.insert(9)
FH2.insert(6)

FH.union(FH2)
print(f'New min key: {FH.min.key}')