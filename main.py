import queue_class
import queue_sorted
import queue_low_memory
import numpy as np
import bisect


# orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]
# print(orders)

# test1 = queue_low_memory.Solution()
# res = test1.getNumberOfBacklogOrders(orders)
# print(res)

# orders2 = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]
# test2 = queue_low_memory.Solution()
# res2 = test2.getNumberOfBacklogOrders(orders2)
# print(res2)
# print(999999984 % (pow(10,9) + 7))

# orders3 = [[1,29,1],[22,7,1],[24,1,0],[25,15,1],[18,8,1],[8,22,0],[25,15,1],[30,1,1],[27,30,0]]
# test3 = queue_low_memory.Solution()
# res3 = test3.getNumberOfBacklogOrders(orders3)
# print(res3)

orders4 = [[536030421,863650261,1],[494834809,228942285,1],[617117972,849543087,1],[565939973,768270609,1],[396069739,839001992,1],[139298597,184236981,1],[608516037,403680450,1],[968957334,269554413,1],[802462170,379958256,1],[628543886,928174830,1]]
test4 = queue_low_memory.Solution()
res4 = test4.getNumberOfBacklogOrders(orders4)
print(res4)