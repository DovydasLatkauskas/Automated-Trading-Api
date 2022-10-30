from Trading212 import CFD

email = "dovydas.latkauskas@gmail.com"
# can be replaced with      email = input("input email: ")
password = "manoaccountas123"
# can be replaced with      password = input("input password: ")

stock = "Apple"

def buy(stock, amount):
    trading = CFD(email, password)
    trading.buy_stock(stock, amount)

buy(stock, 5)