import queue_class

orders = [[10,5,0],[15,2,1],[25,1,1],[30,4,0]]

test1 = queue_class.Solution()
res = test1.getNumberOfBacklogOrders(orders)
print(res)

orders2 = [[7,1000000000,1],[15,3,0],[5,999999995,0],[5,1,1]]
test2 = queue_class.Solution()
res2 = test2.getNumberOfBacklogOrders(orders2)
print(res2)

