# https://leetcode.com/problems/number-of-orders-in-the-backlog/description/

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

        #function to add orders to a queue sorted in an increasing order
        def queue_inc_add_item(queue_inc, item_price, item_amount):
            orders = [item_price]*item_amount
            if queue_inc == [] :                        #queue jest pusta -> zrobic liste dodac orders
                queue_inc = orders
                return queue_inc
            queue_inc.extend(orders)
            queue_inc.sort()
            return queue_inc

        #function to add orders to a queue sorted in a decreasing order
        def queue_dec_add_item(queue_dec, item_price, item_amount):
            orders = [item_price]*item_amount
            if queue_dec == [] :                        #queue jest pusta -> zrobic liste dodac orders
                queue_dec = orders
                return queue_dec
            queue_dec.extend(orders)
            queue_dec.sort(reverse=True)
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