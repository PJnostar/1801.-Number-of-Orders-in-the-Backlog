# https://leetcode.com/problems/number-of-orders-in-the-backlog/description/

import bisect

class Solution(object):
    def getNumberOfBacklogOrders(self, orders):
        """
        :type orders: List[List[int]]       [price, amount, type]
        :rtype: int
        """
        #queue_inc -> [ list of orders sorted by increasing prices ]
        #item -> [price, amount, type]

        #   BACKLOG_BUY has to be in DECREASING order because:
        #   "if the order is a sell order, you look at the buy order with the largest price in the backlog. 
        #   If that buy order's price is larger than or equal to the current sell order's price, they will 
        #   match and be executed, and that buy order will be removed from the backlog. Else, the sell order 
        #   is added to the backlog."

        #   BACKLOG_SELL has to be in INCREASING order because:
        #   "If the order is a buy order, you look at the sell order with the smallest price in the backlog.
        #   If that sell order's price is smaller than or equal to the current buy order's price, they will 
        #   match and be executed, and that sell order will be removed from the backlog"


        # funkcja znajdujaca indeks, w ktorym miejscu trzeba wstawic zamowienia, dla rosnących zamowien 
        def find_where_to_add_order_in_increasing_order(queue_inc, item_price):
            n = len(queue_inc)
            if (queue_inc[n-1] <= item_price):          #wstawic orders na koniec listy
                index_to_add = n
                # queue_inc = queue_inc + orders
                return index_to_add
            if (queue_inc[0] >= item_price):            #wstawic orders na początek listy
                index_to_add = 0
                # queue_inc = orders + queue_inc
                return index_to_add
            for i in range(0,n-1):
                if (queue_inc[i] <= item_price and queue_inc[i+1] > item_price ): #wstawić order gdzieś w środku
                    # queue_inc = queue_inc[:i+1] + orders + queue_inc[i+1:]
                    index_to_add = i
                    break
            return index_to_add
        
        # funkcja znajdujaca indeks, w ktorym miejscu trzeba wstawic zamowienia, dla rosnących zamowien 
        #BISECTEM  
        def find_where_to_add_order_in_increasing_order_bisect(queue_inc, item_price):
            n = len(queue_inc)
            index_to_add = bisect.bisect_left(queue_inc, item_price)
            return index_to_add
        
        # funkcja znajdujaca indeks, w ktorym miejscu trzeba wstawic zamowienia, dla malejacych zamowien
        def find_where_to_add_order_in_decreasing_order(queue_inc, item_price):
            n = len(queue_inc)
            if (queue_inc[n-1] >= item_price):          #wstawic orders na koniec listy
                index_to_add = n
                return index_to_add
            if (queue_inc[0] <= item_price):            #wstawic orders na początek listy
                index_to_add = 0
                return index_to_add
            for i in range(0,n-1):
                if (queue_inc[i] >= item_price and queue_inc[i+1] < item_price ): #wstawić order gdzieś w środku
                    # queue_inc = queue_inc[:i+1] + orders + queue_inc[i+1:]
                    index_to_add = i
                    break
            return index_to_add

        #function to add orders to a queue sorted in an increasing order
        def queue_inc_add_item(queue_inc, item_price, item_amount):
            n = len(queue_inc)
            orders = [item_price]*item_amount
            if queue_inc == [] :                        #queue jest pusta -> zrobic liste dodac orders
                queue_inc = orders
                return queue_inc
            index_to_add = find_where_to_add_order_in_increasing_order(queue_inc, item_price)
            queue_inc = queue_inc[:index_to_add] + orders + queue_inc[index_to_add:]
            return queue_inc

        #function to add orders to a queue sorted in a decreasing order
        def queue_dec_add_item(queue_dec, item_price, item_amount):
            n = len(queue_dec)
            orders = [item_price]*item_amount
            if queue_dec == [] :                        #queue jest pusta -> zrobic liste dodac orders
                queue_dec = orders
                return queue_dec
            index_to_add = find_where_to_add_order_in_decreasing_order(queue_dec, item_price)
            queue_dec = queue_dec[:index_to_add] + orders + queue_dec[index_to_add:]
            return queue_dec
        
        #function to buy items from backlog_sell
        #order contains a single order[price, amount, type], not the entire list of them
        def buy_items_from_backlog_sell(backlog_sell, backlog_buy, order):
            for i in range(0, order[1]):
                if (backlog_sell == []):
                    backlog_buy = queue_dec_add_item(backlog_buy, order[0], 1)
                else:
                    if (order[0] >= backlog_sell[0]):       #order is executed == element from backlog_sell is deleted
                        backlog_sell.pop(0)
                    else:
                        backlog_buy = queue_dec_add_item(backlog_buy, order[0], 1)
            return [backlog_buy, backlog_sell]

        #function to sell items from backlog_buy
        # def sell_items_from_backlog_buy(backlog_buy, order):
        def buy_items_from_backlog_buy(backlog_sell, backlog_buy, order):
            for i in range(0, order[1]):
                if (backlog_buy == []):
                    backlog_sell = queue_inc_add_item(backlog_sell, order[0], 1)
                else:
                    if (order[0] <= backlog_buy[0]):       #order is executed == element from backlog_sell is deleted
                        backlog_buy.pop(0)
                    else:
                        backlog_sell = queue_inc_add_item(backlog_sell, order[0], 1)
            return [backlog_buy, backlog_sell]


        #wlasciwa czesc kodu wykonujaca zadanie
        backlog_buy = []
        backlog_sell = []
        for order in orders:
            print(order)
            if (order[2] == 0):
                [backlog_buy, backlog_sell] = buy_items_from_backlog_sell(backlog_sell, backlog_buy, order)
            elif (order[2] == 1):
                [backlog_buy, backlog_sell] = buy_items_from_backlog_buy(backlog_sell, backlog_buy, order)
        print("backlog_buy: ", backlog_buy)
        print("backlog_sell: ", backlog_sell)

        return (len(backlog_sell) + len(backlog_buy))%(pow(10,9)+7)
""" 
        queue_inc_test = [1,2,3,4,5]
        item = [7,3,1]
        N = queue_inc_add_item(queue_inc_test, item[0], item[1])
        print(N)

        queue_dec_test = [5,4,3,2,1]
        item = [7,3,1]
        N = queue_dec_add_item(queue_dec_test, item[0], item[1])
        print("item= ", item[0], "N = ",  N)
        item = [5,3,1]
        N = queue_dec_add_item(queue_dec_test, item[0], item[1])
        print("item= ", item[0], "N = ",  N)
        item = [3,3,1]
        N = queue_dec_add_item(queue_dec_test, item[0], item[1])
        print("item= ", item[0], "N = ",  N)
        item = [1,3,1]
        N = queue_dec_add_item(queue_dec_test, item[0], item[1])
        print("item= ", item[0], "N = ",  N)
        item = [0,3,1]
        N = queue_dec_add_item(queue_dec_test, item[0], item[1])
        print("item= ", item[0], "N = ",  N)
 """