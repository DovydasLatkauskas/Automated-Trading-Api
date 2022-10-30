# imports       imports       imports       imports       imports       
from Trading212 import Invest # trading212 but locally

import yahoo_fin.stock_info as si

import datetime

from random import randint #just for testing, remove after

# from open_hours import is_open # uncomment after testing

def is_open(): # remove this after testing
    return True




# parameters        parameters        parameters        parameters        parameters        parameters        

stock = "Apple" # PARAMETER   PUT THE NAME AS IT APPEARS ON TRADING212!!! E.G Apple instead of AAPL

stock_short_name = "AAPL" # PARAMETER 4 letter name of the stock

parameter_max_transaction_sum = 8 # PARAMETER    what % of the portfolio total value can be used in 1 transaction

buy_sell_frequency = 30 # PARAMETER    in seconds how frequently does the algorithm make a decisions to buy or sell



# keeping track of portfolio details     keeping track of portfolio details     keeping track of portfolio details

allocated_cash = 20000 # PARAMETER   allocate the cash the algorithm can use

free_cash = allocated_cash # how much remaining cash the algo has to buy stocks with



open_position_num = 0 # how many shares have we got (change before starting if > 0)

# class Sold: # no longer used
#     def __init__(self, timestamp, sold_for, amount): #sold_for is individual stock value
#         self.timestamp = timestamp
#         self.sold_for = sold_for
#         self.amount = amount

# class Bought: # no longer used
#     def __init__(self, timestamp, bought_for, amount): #sold_for is individual stock value
#         self.timestamp = timestamp
#         self.bought_for = bought_for
#         self.amount = amount


# log in details           log in details                  log in details 


email = "dovydas.latkauskas@gmail.com"
# can be replaced with      email = input("input email: ")
password = "manoaccountas123"
# can be replaced with      password = input("input password: ")





def buy(stock, amount):
    trading = Invest(email, password) # For practice account
    trading.buy_stock(stock, amount)

def sell(stock, amount):
    print (f"selling {amount} stocks (only simulated)")
    # trading = Invest(email, password) # For practice account
    # trading.sell_stock(stock, amount)




def has_stock(stock):
    global open_position_num

    if open_position_num > 0:
        return True
    else:
        return False

def get_stock_price(stock_short_name): # function to get Stock price
    stock_price = si.get_live_price(stock_short_name)
    return stock_price


parameter_max_transaction_sum /= 100 # converts initial mts % to numbers

def get_max_transaction_sum(stock_price):
    global parameter_max_transaction_sum
    global portfolio_value # just for testing

    portfolio_value = free_cash + open_position_num * stock_price
    max_transaction_sum = parameter_max_transaction_sum * portfolio_value
    return max_transaction_sum




def algo(stock): # simulation of the algorithm just to get a value, will be replaced by a call for the real algo
    delta = randint(1, 100) # now always outputs a positive value to buy

    if delta > 0:
        return True
    if delta < 0:
        return False
    if delta == 0:
        return 0



# nested lists to keep track of when and how much bought/sold
# each element is [amount, stock_price, timestamp]

sold = []
bought = []


def is_mistake(transaction_type, stock_price):
    if transaction_type == "bought":
        return False # can't make mistakes when buying
        # if sold == []:
        #     return False
        # elif sold [-1][1] < stock_price:
        #     return True

    elif transaction_type == "sold":
        if bought [-1][1] > stock_price:
            return True


def mistakes(transaction_type, amount, stock_price, timestamp):
    # # can't make mistakes when buying
    # if transaction_type == "bought":
    #     if sold [-1][1] < stock_price:
    #         print (f"mistake at {timestamp}, {transaction_type} {amount} shares for {stock_price}, but last sold for {sold[-1][1]")

    if transaction_type == "sold":
        if bought [-1][1] > stock_price:
            return (f"mistake at {timestamp}, {transaction_type} {amount} shares for {stock_price}$, that were bought for {bought[-1][1]}$ at {bought[-1][2]}. Amount lost per share = {bought[-1][1] - stock_price}$\n")




def algo_decision(): # decides whether to buy or to sell the shares it has and how many
    global portfolio_value # just for testing

    global stock
    global stock_short_name
    global free_cash
    global open_position_num


    if is_open(): # checks whether or not regular market is open
        algo_ans = algo(stock) # algorithm output
        stock_price = get_stock_price(stock_short_name)
        max_transaction_sum = get_max_transaction_sum(stock_price)

        if algo_ans: # if algo outputs True (price should go up)
            amount = free_cash // stock_price
            if amount * stock_price > max_transaction_sum:
                amount = max_transaction_sum // stock_price
                if free_cash < amount * stock_price:
                    amount = free_cash // stock_price
            free_cash -= amount * stock_price
            buy(stock, amount)
            open_position_num += amount
            
            timestamp = datetime.datetime.now()
            bought.append([amount, stock_price, timestamp])

            # # can't make mistakes when buying
            # transaction_type = "bought"
            # if is_mistake(transaction_type, stock_price):
            #     mistake = mistakes(transaction_type, amount, stock_price, timestamp)
            #         f = open("mistakes.txt", "a")
            #         f.write(mistake)
            #         f.close()
            

        elif not algo_ans: # if algo outputs False (price should go down)
            if has_stock(stock):
                amount = open_position_num
                if amount * stock_price > max_transaction_sum:
                    amount = max_transaction_sum // stock_price
                free_cash += amount * stock_price
                sell(stock, amount)
                open_position_num -= amount

                timestamp = datetime.datetime.now()
                sold.append([amount, stock_price, timestamp])

                transaction_type = "sold"
                if is_mistake(transaction_type, stock_price):
                    mistake = mistakes(transaction_type, amount, stock_price, timestamp)
                    f = open("mistakes.txt", "a")
                    f.write(mistake)
                    f.close()

            elif not has_stock(stock): # if we have nothing to sell
                print("nothing to sell") # maybe remove the print() and do nothing

        elif algo_ans == 0: # fringe case if price doesnt change
            print("no change in price") # maybe remove the print() and do nothing
    # else: print("market is closed") # maybe remove the print() and do nothing

    # print ("done") # just for testing
    # print (f"open position number: {open_position_num}") # just for testing
    # print (f"portfolio total value: {portfolio_value}") # just for testing
    # print ("stock price: ", stock_price) # just for testing
    # print ("algo answer: ", algo_ans) # just for testing
    # print ("open position num: ", open_position_num) # just for testing
    # print ("free cash: ", free_cash) # just for testing
    # print ("max trans sum: ", max_transaction_sum) # just for testing
    # print ("amount: ", amount) # just for testing



# print("done")


# needs to be done:
#    1st part:
#       logging in works /// done
#       buying and selling works /// buying done BUT NOT SELLING
#       getting stock_price /// done
#       max_transaction_sum 8% nuo portfelio vertes /// done

#   2nd part:
#       loop of the algo working /// done
#       must work only when market is open /// done, just have to uncomment
#       mistake display (when sold at a loss)