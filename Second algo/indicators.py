import yahoo_fin.stock_info as si
import yfinance as yf

import pandas as pd

import operator

from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

from datetime import datetime
from datetime import time
from datetime import timezone
from datetime import date
from datetime import timedelta 

company = input("company: ")

company_yf = yf.Ticker(company)

current_stock_price = si.get_live_price(company)


#//////////////////////////date and time//////////////////////////////////////////////////////////////////


days14_date = date.today() - timedelta(days = 14)
days14_date = days14_date.strftime("%m/%d/%Y")

tommorow_date = date.today() - timedelta(days = -1)
tommorow_date = tommorow_date.strftime("%m/%d/%Y")

# print(days14_date)
# print(tommorow_date)


current_date1 = date.today().strftime("%m/%d/%y")
current_month = current_date1[0:2]
current_day = current_date1[3:5]
current_year = "20" + str(current_date1[6:8])

yesterday_date1 = date.today() - timedelta(days = -1)
yesterday_date1 = yesterday_date1.strftime("%m/%d/%y")
yesterday_month = yesterday_date1[0:2]
yesterday_day = yesterday_date1[3:5]
yesterday_year = "20" + str(yesterday_date1[6:8])

formated_current_date1 = current_month + "/" + current_day + "/" + current_year

formated_yesterday_date1 = yesterday_month + "/" + yesterday_day + "/" + yesterday_year

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def ST14days(): #stock price table for the last 14 days
    days14_stock_price_table = si.get_data(company, start_date = days14_date, end_date = tommorow_date)
    return days14_stock_price_table



def stock_gain_loss_avg(ST): #produces the avg stock price gain and loss of the last 14 days, returns a tuple (avg gain, avg loss)
    stock_price_change_open_stock_list = []
    stock_price_change_gain_list = []
    stock_price_change_loss_list = []
    row_count = ST.shape
    row_count = row_count[0]

    for i in range (0, row_count):
        open_stock = ST.iat[i, 0]
        stock_price_change_open_stock_list.append(open_stock)
    for j in range (0, len(stock_price_change_open_stock_list)-1):
        if stock_price_change_open_stock_list[j + 1] > stock_price_change_open_stock_list[j]:
            stock_price_change_gain_list.append((stock_price_change_open_stock_list[j + 1] / stock_price_change_open_stock_list[j]-1) * 100)
        else:
            stock_price_change_loss_list.append((stock_price_change_open_stock_list[j] / stock_price_change_open_stock_list[j + 1]-1) * 100)
    avg_gain = sum(stock_price_change_gain_list) / len(stock_price_change_gain_list)
    avg_loss = sum(stock_price_change_loss_list) / len(stock_price_change_loss_list)
    return avg_gain, avg_loss
        
#gain_loss_14days_tuple = stock_price_change_14days()
#avg_gain_14days = gain_loss_14days_tuple[0]
#avg_loss_14days = gain_loss_14days_tuple[1]

def avg_gain_14days():
    gain_loss_14days_tuple = stock_gain_loss_avg(ST14days())
    return gain_loss_14days_tuple[0]

def avg_loss_14days():
    gain_loss_14days_tuple = stock_gain_loss_avg(ST14days())
    return gain_loss_14days_tuple[1]


#/////////////////////////////////////////////// yfinance for 15 minute rsi /////////////////////////////////////////

def ST15min():
    minutes15_stock_price_table = company_yf.history("15m", "1m")
    return minutes15_stock_price_table

def ST30min():
    minutes30_stock_price_table = company_yf.history("30m", "1m")
    return minutes30_stock_price_table
    
def ST60min():
    minutes60_stock_price_table = company_yf.history("60m", "1m")
    return minutes60_stock_price_table

def ST90min():
    minutes90_stock_price_table = company_yf.history("90m", "1m")
    return minutes90_stock_price_table




def ST12min():
    minutes12_stock_price_table = company_yf.history("15m", "1m")
    minutes12_stock_price_table = minutes12_stock_price_table.drop(minutes12_stock_price_table.index[[0, 1, 2]])
    return minutes12_stock_price_table

def ST26min():
    minutes26_stock_price_table = company_yf.history("30m", "1m")
    minutes26_stock_price_table = minutes26_stock_price_table.drop(minutes26_stock_price_table.index[[0, 1, 2, 3]])
    return minutes26_stock_price_table




def avg_gain_15min():
    gain_loss_15min_tuple = stock_gain_loss_avg(ST15min())
    return gain_loss_15min_tuple[0]

def avg_loss_15min():
    gain_loss_15min_tuple = stock_gain_loss_avg(ST15min())
    return gain_loss_15min_tuple[1]

def avg_gain_90min():
    gain_loss_90min_tuple = stock_gain_loss_avg(ST90min())
    return gain_loss_90min_tuple[0]

def avg_loss_90min():
    gain_loss_90min_tuple = stock_gain_loss_avg(ST90min())
    return gain_loss_90min_tuple[1]

def SPsum(ST):
    SPsum = ST['Open'].sum()
    return SPsum

#///////////////////////////////// final indicators ///////////////////////////////////////////////////////////////////////////////////

def rsi(avg_gain, avg_loss):
    rsi = 100 - 100 / (1+ avg_gain / avg_loss)
    return rsi

#print (rsi(avg_gain_14days(), avg_loss_14days()))

#print (rsi(avg_gain_15min(), avg_loss_15min()))

#print (rsi(avg_gain_90min(), avg_loss_90min()))

def SMA(ST):
    SPs = SPsum(ST)
    row_count = ST.shape
    row_count = row_count[0]
    periodN = row_count
    SMA = SPs / periodN
    return SMA

#print (SMA(ST90min()))


def EMA(ST):
    row_count = ST.shape
    row_count = row_count[0]
    periodN = row_count
    EMA_now = 0
    for i in range (0, periodN):
        open_stock = ST.iat[i, 0]
        EMA_now = (open_stock * (2 / (1+periodN) ) ) + EMA_now * (1- (2 / (1+periodN) ) )
    return EMA_now


#print (EMA(ST90min()))

def BOLU(ST):
    row_count = ST.shape
    row_count = row_count[0]
    periodN = row_count
    moving_average = ST['Open'].rolling(window=periodN).mean()
    standard_deviation = ST['Open'].rolling(window=periodN).std()
    bolu = moving_average + 2 * standard_deviation
    bolu = bolu.sum()
    return bolu

def BOLD(ST):
    row_count = ST.shape
    row_count = row_count[0]
    periodN = row_count
    moving_average = ST['Open'].rolling(window=periodN).mean()
    standard_deviation = ST['Open'].rolling(window=periodN).std()
    bolu = moving_average - 2 * standard_deviation
    bolu = bolu.sum()
    return bolu

#print (BOLU(ST90min()))

#print (BOLD(ST90min()))

def MACD(ST1, ST2):
   EMA_12_periods = EMA(ST1)
   EMA_26_periods = EMA(ST2)
   MACD = EMA_12_periods - EMA_26_periods
   return MACD

#print (MACD(ST12min(), ST26min()))

def MACDsignal():
    MACDsignal_list = []
    for k in range (0, 9):
        first_stock_table = ST30min()
        first_stock_table = first_stock_table.iloc[8+k:21+k]
        second_stock_table = ST60min()
        second_stock_table = second_stock_table.iloc[25+k:51+k]
        MACDvalue = MACD(first_stock_table, second_stock_table)
        MACDsignal_list.append(MACDvalue)
    row_count = len(MACDsignal_list)
    EMA = 0
    for i in range (0, row_count):
        MACDvalue1 = MACDsignal_list[i]
        EMA = (MACDvalue1 * (2 / (1+row_count) ) ) + EMA * (1- (2 / (1+row_count) ) )
    return EMA

#print (MACDsignal())