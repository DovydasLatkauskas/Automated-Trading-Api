import yfinance as yf

import pandas as pd

import math

def Main():
    isgoodinvestment()

companyname = input("Company name:")

company = yf.Ticker(companyname)

def businesssummary(): #business summary (text)
    lbs = company.info['longBusinessSummary']
    return lbs

def shareprice(): #share price right now
    shareP = company.history("5d")
    shareP = shareP.iat[4, 0]
    return shareP

def sharesOutstanding(): #shares quantity right now
    shareQ = company.info["sharesOutstanding"] #sita atskirai, nes paskui eps reiks skaiciuot
    return shareQ

def marketcap():
    shareQ = sharesOutstanding()
    shareP = shareprice()
    marketC = shareQ * shareP # market cap = share quantity * share price
    return marketC

def Beta(): # finds the beta of a company
    companybeta = company.info ["beta"]
    return companybeta

def netIncome(): # last quarter net income
    netinc = company.quarterly_financials
    netinc = netinc.iat[4,0]
    return netinc

def NetChangeInCash():
    ncic = company.quarterly_cashflow.iat[7,0]
    return ncic

def max3inlist(alist): #used in changeincashreasons, finds top 3 numbers in a list (in order)
    max3list = []
    for i in range (0, 3):
        maxvalue = max(alist)
        max3list.append(maxvalue)
        x = alist.index(maxvalue)
        alist[x] = 0
    return max3list


def changeInCashReasons(): # this quarter's top 3 reasons for change in cash ( counted with abs(), but shown without abs() )
    cflow = company.quarterly_cashflow
    valuelist = []
    absvaluelist = []
    for i in range (0, len(cflow)):
        if math.isnan(cflow.iat[i, 0]):
            valuelist.append(0)
            continue
        line = int(cflow.iat[i, 0])
        valuelist.append(line)
    reasonNameAr = company.quarterly_cashflow.index.values
    for j in range (0, len(valuelist)):
        absvaluelist.append(abs(valuelist[j]))
    absvaluelistcopy = absvaluelist.copy()
    max3 = max3inlist(absvaluelistcopy)
    displayList = ["Top 3 reasons for change in cash:"]
    for k in range (0, 3):
        x = max3[k] #takes a number from top 3 reasons values
        positionofreason = absvaluelist.index(x) #finds the position of the reason value in valuelist
        displayList.append(str(reasonNameAr[positionofreason]) + " " + str(valuelist[positionofreason]))
    return displayList

def sharePchange(): #change in share price during the last 3 months
    sharePnow = shareprice()
    sharePthen = company.history("3mo")
    sharePthen = sharePthen.iat[0,3]
    sharePchpr = sharePnow / sharePthen * 100 - 100
    sharePchpr = str(sharePchpr) + "%"
    return sharePchpr

def predEPS(): #predicted EPS of this quarter
    EPS = company.calendar
    EPS = EPS.iat[1,0]
    return EPS

def prevEPS(): # previous quarter earnings divided by current amount of shares (will be wrong if sharesQ changed lol)
    prevEarn = company.quarterly_earnings.iat[3,1]
    shareQ = sharesOutstanding()
    prevEPS = prevEarn / shareQ
    return prevEPS

def predRev (): #preditcted avg revenue of this quarter
    predRev = company.calendar
    predRev = predRev.iat[4,0]
    return predRev

def prevRev(): #revenue of last quarter
    prevRev = company.quarterly_earnings.iat[3,0]
    return prevRev

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#

#print (businesssummary())

def marcapsize():
    marC =  marketcap() // 1000000000
    marC = int(marC)
    if marC < 2: marC = "small " + str(marC) + "B"
    elif 2 <= marC < 10: marC = "medium " + str(marC) + "B"
    elif marC >= 10: marC = "large " + str(marC) + "B"
    string = "market cap size is: " + marC
    return string

print (marcapsize())

print(changeInCashReasons())

print ("share price change in the last 3 months: " +  str(sharePchange()))

SQ = [] # stock quality list, if all = true its a good stock if any parameters = false, then its a bad stock



if Beta() > 0.5: SQ.append(True)
else: SQ.append(False)

if netIncome() > 0: SQ.append(True)
else: SQ.append(False)

if NetChangeInCash() > 0: SQ.append(True)
else: SQ.append(False)

if predEPS() > prevEPS(): SQ.append(True)
else: SQ.append(False)

if predRev() > prevRev(): SQ.append(True)
else: SQ.append(False)

SQL = []

def stockquality():
    for i in range (0, SQ.count(False)):
        SQ.insert(SQ.index(False) + 1, "orange")
        x = SQ.index(False)
        SQ.remove(False)
        SQL.append(x)

stockquality()

reasons = []

def isgoodinvestment():
    if SQL == []: print("Kompanija tinkama")
    else:
        for i in range (0, len(SQL)):
            if SQL [i] == 0: reasons.append("beta is less than 0.5, beta: " + str(Beta()))
            elif SQL [i] == 1: reasons.append("net income is negative, net income: " + str(netIncome()))
            elif SQL [i] == 2: reasons.append("net change in cash is negative, NCIC: " + str(NetChangeInCash()))
            elif SQL [i] == 3: reasons.append("predicted EPS is lower than previous EPS, predicted EPS: " + str(predEPS()) + " previous EPS: " + str(prevEPS()))
            elif SQL [i] == 4: reasons.append("predicted revenue is lower than previous revenue, predicted revenue: " + str(predRev()) + " previous revenue: " + str(prevRev()))
        print ("Kompanija netinkama, nes:" + str(reasons))