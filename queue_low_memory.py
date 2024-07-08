# https://leetcode.com/problems/number-of-orders-in-the-backlog/description/
#Attempt to write the backlog so that it doesnt eat a ton of memory.

import numpy as np

class Solution(object):
    def getNumberOfBacklogOrders(self, orders):
        """
        :type orders: List[List[int]]       [price, amount, type]
        :rtype: int
        """
        #queue_inc -> [ list of orders sorted by increasing prices ]
        #item -> [price, amount, type]
        #backlog = [price, amount] - sorted by price

        # buy : 100, 90, 50, 20
        # sell: 10, 30, 40, 50
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
            if queue_inc.size == 0 :                            #queue jest pusta -> zrobic liste dodac orders
                return np.array([[item_price, item_amount]])
            if (item_price in queue_inc[:,0]):                  #sprawdza czy dana cena jest w logu. jesli jest to zwieksza jej ilosc
                i = np.where(queue_inc[:,0] == item_price)
                queue_inc[i[0],1] += item_amount                #queue_inc[np.where(queue_inc[:,0] == item_price),1] += item_amount też działa
            else:                                               #jesli tworzy nowy order, trzeba posortowac
                queue_inc = np.append(queue_inc, [[item_price, item_amount]], axis=0)
                queue_inc = queue_inc[queue_inc[:,0].argsort()]
            return queue_inc

        #function to add orders to a queue sorted in a decreasing order
        def queue_dec_add_item(queue_dec, item_price, item_amount):
            if queue_dec.size == 0 :                            #queue jest pusta -> zrobic liste dodac orders
                queue_dec = np.zeros((1,2))
                return np.array([[item_price, item_amount]])
            if (item_price in queue_dec[:,0]):                  #sprawdza czy dana cena jest w logu. jesli jest to zwieksza jej ilosc
                i = np.where(queue_dec[:,0] == item_price)
                queue_dec[i[0],1] += item_amount                #queue_inc[np.where(queue_inc[:,0] == item_price),1] += item_amount też działa
            else:                                               #jesli tworzy nowy order, trzeba posortowac
                queue_dec = np.append(queue_dec, [[item_price, item_amount]], axis=0)
                queue_dec = queue_dec[queue_dec[:,0].argsort()[::-1]]
            return queue_dec
        
        #function to buy items from backlog_sell
        def buy_items_from_backlog_sell(backlog_buy, backlog_sell, order):
            if backlog_sell.size == 0 :                                                 #backlog_sell jest pusty -> 
                backlog_buy = queue_dec_add_item(backlog_buy, order[0], order[1])
            else:
                #this part gets complicated
                #Trzeba sprawdzić kilka rzeczy:
                # 1) czy wartosc zamowienia order jest wystarczajaca, żeby kupić z backlog_sell. Jeśli nie, to ordery 
                #    wpadaja do backlog_buy
                # 2) czy ilość zamowień w order jest wieksza niz ilosc zamowien w backlog_sell. Jesli tak, to tylko 
                #    odejmuje ich ilosc w backlogu 
                # 3) Jesli ilosc orderow jest wieksza niz zamowien w backlog_sell, to odejmuje ilosc zamowien w backlog_sell 
                #    od orderow oraz kasuje cale zamowienie w backlog_sell. Nastepnie sprawdzam, czy backlog_sell jest pusty. 
                #    Jesli jest pusty, to dodaje pozostale orders do backlog_buy.
                # 4) Wracam do kroku 1 jesli ilosc zamowien w order>0
                while(order[1] > 0):
                    if (backlog_sell[0,0] > order[0]):
                        backlog_buy = queue_dec_add_item(backlog_buy, order[0], order[1])
                        break
                    else:
                        if (backlog_sell[0,1] > order[1]):                                     #jesli ilosc zamowienia w logu jest wystarczajaca
                            backlog_sell[0,1] -= order[1]                                       #to tylko odejmuje ilosci
                            break
                        else:                                                                   #jesli nie, to dodaje zamowienia do logu buy w ilosci
                                                                                                #roznicy (order[1]-backlog_sell[0,1]), a w logu sell zeruje
                            order[1] -= backlog_sell[0,1]
                            backlog_sell = backlog_sell[1:, :]
                            if (backlog_sell.size == 0):
                                backlog_buy = queue_dec_add_item(backlog_buy, order[0], order[1])
                                break
                
            return [backlog_buy, backlog_sell]

        #function to sell items from backlog_buy
        def buy_items_from_backlog_buy(backlog_buy, backlog_sell, order):
            if backlog_buy.size == 0 :                                                 #backlog_sell jest pusty -> 
                backlog_sell = queue_inc_add_item(backlog_sell, order[0], order[1])
            else:
                while(order[1] > 0):
                    if (backlog_buy[0,0] < order[0]):
                        backlog_sell = queue_inc_add_item(backlog_sell, order[0], order[1])
                        order[1] = 0
                    else:
                        if (backlog_buy[0,1] > order[1]):                                     
                            backlog_buy[0,1] -= order[1]                                                                  
                            order[1] = 0
                        else:
                            order[1] -= backlog_buy[0,1]
                            backlog_buy = backlog_buy[1:, :]
                            if (backlog_buy.size == 0):
                                backlog_sell = queue_inc_add_item(backlog_sell, order[0], order[1])
                                break
            return [backlog_buy, backlog_sell]


        #wlasciwa czesc kodu wykonujaca zadanie
        backlog_buy = np.array([[]])
        backlog_sell = np.array([[]])
        """ 
        test tworzenia logow
        for order in orders:
            if (order[2] == 0):
                backlog_buy = queue_dec_add_item(backlog_buy, order[0], order[1])
            elif (order[2] == 1):
                backlog_sell = queue_inc_add_item(backlog_sell, order[0], order[1]) 
        """
        for order in orders:
            if (order[2] == 0):
                [backlog_buy, backlog_sell] = buy_items_from_backlog_sell(backlog_buy, backlog_sell, order)
            else:
                [backlog_buy, backlog_sell] = buy_items_from_backlog_buy(backlog_buy, backlog_sell, order)
        
        print("backlog_buy: \n", backlog_buy)
        print("backlog_sell: \n", backlog_sell)
        # return (sum(backlog_sell[:,1]) + sum(backlog_buy[:,1]))%(pow(10,9)+7)
        sum_of_logs = 0
        if (backlog_buy.size != 0):
            sum_of_logs += sum(backlog_buy[:,1])
        if (backlog_sell.size != 0):
            sum_of_logs += sum(backlog_sell[:,1])
        return sum_of_logs%(pow(10,9)+7)
