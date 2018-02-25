# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 09:42:04 2018

@author: Kalyan Parthasarathy
"""

# Logic: -
# *********
# 
# 1. Create a class (SecurityTransaction) for Security details - Ticker, Qty, Buying/Sell, Executed price, Timestamp, Total In/Out, Weighted Average Price and P/L for Sold transactions
# 2. Create a class (StockPortfolio) for Security List - total money available (double), stock transactions list, Securities holdings and Securities WAP. Initialize the total available money to be $100,000,000 ($100 million)
# 	2.a Create a method to purchase the stock:
# 		Inputs - Symbol, Buy/Sell, Qty, Price
# 		Activity:
# 			- Find the total purchase price (for purchase)
# 			- Check if the user has enough balance to make the purchase. If not, send a message to the buyer
# 			- Subtract the purchase price from the total available money for purchasing stocks (Buy) and increase the available money for Sell transactions
# 			- Show confirmation to the user
# 	2.b Create a method to show transactions (Blotter)
# 		- Iterate through the stock transactions list and display it to the user - Side (Buy/Sell), Ticker, Quantity, Executed Price, Executed Timestamp and Total Money In/Out
# 	2.c Create a method to show P/L
# 		- Get the current ticker prices from Bloomberg
# 		- For each ticker:
# 			- Get the current holdings list and calculate the unrealized gains/loss (iteration) - probably keep a Key/Value data type to track the total UPL
# 			- Get the sold holdings list and calculate the realized gains/loss - probably keep a Key/Value data type to track the total RPL
# 			- Get the average holding price based on the transactions list and store them in Key/Value pair by Ticker
# 	2.d Create a method to get Unrealized profit
# 		Inputs: Ticker
# 		- Calculate Total Invested amount and Total Current value for the ticker
# 		- Return the difference
# 	2.e Create a method to get Realized profit
# 		Inputs: Ticker
# 		- Get only the sold transactions list
# 		- for each sold stock of the ticker, get the realized profit and sum it up
# 		- Calculate total invested amount and total sold value
# 		- Return the difference
# 	2.f Create a method to get stock price (from Bloomberg)
# 		Inputs: Ticker
# 		- Find the stock price
# 		- Return the value as float
# 3. Create the main code to show the menu and perform the activity based on the user selection (loop this one until the user selects to quit the program)


############## IMPORT STATEMENTS ##############

import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from babel.numbers import format_currency

# Set this to True to print debug statements
enableDebug = False;

# List of Securities used for this program - AAPL,  AMZN, INTC, MSFT & SNAP but feel free to change below
security1 = "AAPL"
security2 = "AMZN"
security3 = "INTC"
security4 = "MSFT"
security5 = "SNAP"


############## CLASS: SecurityTransaction ##############

class SecurityTransaction:
    def __init__(self):
        self.ticker = ""
        self.qty = 0
        self.activity = ""
        self.factor = 1
        self.execPrice = float(0.0)
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.total = float(0.0)
        self.wap = float(0.0)
        self.profitloss = float(0.0)
        

############## CLASS: StockPortfolio ##############

class StockPortfolio:
    # Constructor
    def __init__(self, security1, security2, security3, security4, security5):
        self.totalAllocatedAmount = float(10000000.00)
        self.securities = {security1:int(0), security2:int(0), security3:0, security4:int(0), security5:int(0)}
        self.securitiesWAP = {security1:float(0.0), security2:float(0.0), security3:float(0.0), security4:float(0.0), security5:float(0.0)}
        self.stockList = []

    
    def purchaseStock(self, ticker, activity, qty, execPrice):
        # Check if it is buy or sell activity
        if activity == 1: # Buy activity
            totalPrice = qty * execPrice
            
            # Check if the user has enough balance
            if totalPrice <= self.totalAllocatedAmount:
                transaction = SecurityTransaction()
                transaction.ticker = ticker
                transaction.qty = qty
                transaction.activity = "BUY"
                transaction.factor = 1
                transaction.execPrice = execPrice
                transaction.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                transaction.total = totalPrice
                
                # Get Weighted Average Price
                self.securitiesWAP[ticker] = ( ( (self.securitiesWAP[ticker] * self.securities[ticker]) + (qty * execPrice) ) / (self.securities[ticker] + qty) )
                transaction.wap = self.securitiesWAP[ticker]
                
                # Unrealized Profit will be calculated on the fly based on the stock price so no need to store
                transaction.profitloss = 0
                
                self.stockList.append(transaction)
                
                # Deduct from available funds
                self.totalAllocatedAmount = self.totalAllocatedAmount - totalPrice
                
                # Increase current holdings detail
                self.securities[ticker] = self.securities[ticker] + qty
                
                print("\n\nYou order is executed. You have purchase {} stocks of {} @ the unit price ${}\n\n".format(qty, ticker, execPrice))
            else:
                print("\n\nYou do not have enough money to make the purchase. Available funds: {}\n\n".format(self.totalAllocatedAmount))
            
        elif activity == -1: # Sell activity
            # Check if the user has enough balance
            if qty < self.securities[ticker]:
                totalPrice = qty * execPrice
                
                transaction = SecurityTransaction()
                transaction.ticker = ticker
                transaction.qty = qty
                transaction.activity = "SELL"
                transaction.factor = -1
                transaction.execPrice = execPrice
                transaction.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                transaction.total = totalPrice
                
                # Get Weighted Average Price
                transaction.wap = self.securitiesWAP[ticker]
                
                # Get Profit/Loss details by calculating the differnce between the weighted average price and selling price * quantity
                transaction.profitloss = (execPrice - self.securitiesWAP[ticker]) * qty
                
                self.stockList.append(transaction)
                
                # Add to the available funds
                self.totalAllocatedAmount = self.totalAllocatedAmount + totalPrice
                
                # Decrease current holdings detail
                self.securities[ticker] = self.securities[ticker] - qty
                
                print("\n\nYou order is executed. You have sold {} stocks of {} @ the unit price ${}\n\n".format(qty, ticker, execPrice))
            else:
                # print("You do not have enough securities to sell. Available Qty: " + self.securities[ticker] + " and you are trying to sell Qty: " + qty)
                print('\n\nYou do not have enough securities to sell. Available Qty:  {}, Qty requested to Sell: {}\n\n'.format(self.securities[ticker], qty))


    def displayBlotter(self):
        # Sort the objects based on the execution timestamp
        self.stockList.sort(key=lambda obj: obj.timestamp, reverse=True)
        moneyInOut = ""

        # Using PrettyTable to display the Blotter
        tableData = PrettyTable(["Buy/Sell", "Ticker", "Quantity", "Executed Price", "Execution Timestamp", "Money In/Out"])

        for stockTrans in self.stockList:
            if stockTrans.factor == 1:
                moneyInOut = "Money Out"
            else:
                moneyInOut = "Money In"
            
            tableData.add_row([stockTrans.activity, stockTrans.ticker, stockTrans.qty, format_currency(round(stockTrans.execPrice, 2), 'USD', locale='en_US'), stockTrans.timestamp, moneyInOut])
            
        print("\n\n")
        print(tableData)
        print("\n\n")

        
    def displayProfitAndLoss(self):
        # Using PrettyTable to display the P&L
        tableData = PrettyTable(["Ticker", "Position", "Market", "WAP", "UPL", "RPL"])
        tableData.add_row([security1, self.securities[security1], format_currency(self.getStockPrice(security1, 'BID'), 'USD', locale='en_US'), format_currency(round(self.securitiesWAP[security1], 2), 'USD', locale='en_US'), format_currency(round(self.getUnrealizedProfit(security1), 2), 'USD', locale='en_US'), format_currency(round(self.getRealizedProfit(security1), 2), 'USD', locale='en_US')])
        tableData.add_row([security2, self.securities[security2], format_currency(self.getStockPrice(security2, 'BID'), 'USD', locale='en_US'), format_currency(round(self.securitiesWAP[security2], 2), 'USD', locale='en_US'), format_currency(round(self.getUnrealizedProfit(security2), 2), 'USD', locale='en_US'), format_currency(round(self.getRealizedProfit(security2), 2), 'USD', locale='en_US')])
        tableData.add_row([security3, self.securities[security3], format_currency(self.getStockPrice(security3, 'BID'), 'USD', locale='en_US'), format_currency(round(self.securitiesWAP[security3], 2), 'USD', locale='en_US'), format_currency(round(self.getUnrealizedProfit(security3), 2), 'USD', locale='en_US'), format_currency(round(self.getRealizedProfit(security3), 2), 'USD', locale='en_US')])
        tableData.add_row([security4, self.securities[security4], format_currency(self.getStockPrice(security4, 'BID'), 'USD', locale='en_US'), format_currency(round(self.securitiesWAP[security4], 2), 'USD', locale='en_US'), format_currency(round(self.getUnrealizedProfit(security4), 2), 'USD', locale='en_US'), format_currency(round(self.getRealizedProfit(security4), 2), 'USD', locale='en_US')])
        tableData.add_row([security5, self.securities[security5], format_currency(self.getStockPrice(security5, 'BID'), 'USD', locale='en_US'), format_currency(round(self.securitiesWAP[security5], 2), 'USD', locale='en_US'), format_currency(round(self.getUnrealizedProfit(security5), 2), 'USD', locale='en_US'), format_currency(round(self.getRealizedProfit(security5), 2), 'USD', locale='en_US')])
        tableData.add_row(["Cash", format_currency(round(self.totalAllocatedAmount, 2), 'USD', locale='en_US'), format_currency(round(self.totalAllocatedAmount, 2), 'USD', locale='en_US'), "", "", ""])
        print("\n\n")
        print(tableData)
        print("\n\n")

        
    def getUnrealizedProfit(self, ticker):
        totalInvestedAmount = float(self.securitiesWAP[ticker] * self.securities[ticker])
        totalCurrentValue = float(self.getStockPrice(ticker, 'BID') * self.securities[ticker])
        
        if enableDebug:
            print("getStockPrice(ticker) is: {}".format(self.getStockPrice(ticker, 'BID')))
            print("self.securitiesWAP[ticker] is: {}".format(self.securitiesWAP[ticker]))
            print("self.securities[ticker] is: {}".format(self.securities[ticker]))
            print("totalInvestedAmount is: {}".format(totalInvestedAmount))
            print("totalCurrentValue is: {}".format(totalCurrentValue))
        
        return float(totalCurrentValue - totalInvestedAmount)

    
    def getRealizedProfit(self, ticker):
        # Get the sell transactions for the ticker
        filteredList = filter(lambda obj: obj.ticker == ticker and obj.factor == -1, self.stockList)
        totalInvestedAmount = float(0.0)
        totalSoldValue = float(0.0)

        for stockTrans in filteredList:
            totalInvestedAmount = float(totalInvestedAmount + (stockTrans.qty * stockTrans.wap))
            totalSoldValue = float(totalSoldValue + (stockTrans.qty * stockTrans.execPrice))

        return float(totalSoldValue - totalInvestedAmount)
        

    # Get the price for the ticker - web scrapping
    def getStockPrice(self, ticker, priceType):
        url = "https://finance.yahoo.com/quote/" + ticker + "?p=" + ticker
        page = requests.get(url)
        stockPrice = float(0.0)

        soup = BeautifulSoup(page.content, 'lxml')
        table = soup.find_all('td', {"data-test": priceType+"-value"})
        soup = BeautifulSoup(str(table), 'lxml')
        span = soup.find("span")

        if span != None:    
            askval = span.text
            ask = askval.split(" ")
            val = ask[0].replace(",","")
            stockPrice = round(float(val), 2)
        elif span is None:
            # Get the Previous close value
            soup = BeautifulSoup(page.content, 'lxml')
            table = soup.find_all('td', {"data-test":  "PREV_CLOSE-value"})
            soup = BeautifulSoup(str(table), 'lxml')
            span = soup.find("span")
            askval = span.text
            ask = askval.split(" ")
            val = ask[0].replace(",","")
            stockPrice = round(float(val), 2)

        return stockPrice


############## MAIN SECTION ##############

if __name__ == "__main__":
    # Instantiate an instance of the main class
    securityTransactions = StockPortfolio(security1, security2, security3, security4, security5)
    
    while True:
        print("\n\nMain Menu:\n")
        print("Trade (1)")
        print("Show Blotter (2)")
        print("Show P/L (3)")
        print("Quit (4)\n\n")
        userInput = input("Please select an option:  ")
    
        if userInput == "1":
            stockTicker = input("\nAvailable stocks to trade - AAPL,  AMZN, INTC, MSFT & SNAP. Enter stock ticker: ")
    
            if stockTicker == security1 or stockTicker == security2 or stockTicker == security3 or stockTicker == security4 or stockTicker == security5:
                tickerPrice = securityTransactions.getStockPrice(stockTicker, 'BID')
                print("\nCurrent trading price of {} is: {}".format(stockTicker, format_currency(tickerPrice, 'USD', locale='en_US')))
    
                while True:
                    operation = int(input("\nEnter you want to Buy (1) or Sell (2) the stock: "))
                    if(operation == 1 or operation == 2):
                        break
                    else:
                        print("\nPlease enter 1 for BUY or 2 for SELL\n")
                
                if(operation == 2):
                    operation = -1
                
                quantity = int(input("\nEnter the quantity that you want to trade: "))
    
                securityTransactions.purchaseStock(stockTicker, operation, quantity, tickerPrice)
            else:
                print("\nPlease enter the correct stock ticker")
                continue
        elif userInput == "2": 
            # Display Blotter
            securityTransactions.displayBlotter()
        elif userInput == "3":
            # Display Profit and Loss statement
            securityTransactions.displayProfitAndLoss()
        elif userInput == "4": # Quit the program
            break
    
