# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 18:53:19 2020

@author: harishangaran

PYTHON OPTION PRICE FOR DIVIDEND PAYING STOCKS
"""

import yfinance as yf
import numpy as np
import scipy.stats as si

'''
The following script calculates European call and put option price of
dividend paying stocks. Spot prices are last close from yahoo finance.

Just call the class and input the variables to get the option prices:
    call option price = getOptionPrice('equity',strickeprice,
                                       time to maturity in years,
                                       interest rate,rate of continous 
                                       dividend paying asset
                                       ,sigma,'call or put').getOptionPrice()
    
    eg: getOptionPrice('MSFT',150,0.5,0.05,0.2,0.25, option = 'call').getOptionPrice()
    eg: getOptionPrice('MSFT',150,0.5,0.05,0.2,0.25, option = 'put').getOptionPrice()
    

K: strike price
T: time to maturity in years
r: interest rate
q: rate of continuous dividend paying asset 
sigma: volatility of underlying asset
'''


class getOptionPrice:
    def __init__(self,equitykey,K,T,r,q,sigma,option ='call'):
        self.key = equitykey
        self.strikePrice = K
        self.timeToMaturity = T
        self.iRate = r
        self.q = q
        self.sigma = sigma
        self.option = option
        self.callSpotPrice()
        self.getOptionPrice()
        
    def callSpotPrice(self):
        self.instrument = yf.Ticker(self.key)
        self.lastDayPrice = self.instrument.history(period='1d')
        self.spotPrice = self.lastDayPrice['Close'][0]
        return self.spotPrice
    def getOptionPrice(self):
        d1 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate -self.q + 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        d2 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate - self.q - 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        if self.option == 'call':
            self.optionPrice = (self.spotPrice * np.exp(-self.q * self.timeToMaturity) * si.norm.cdf(d1, 0.0, 1.0) - self.strikePrice * np.exp(-self.iRate * self.timeToMaturity) * si.norm.cdf(d2, 0.0, 1.0))
            return self.optionPrice,'call',self.key
        if self.option == 'put':
            self.optionPrice = (self.strikePrice * np.exp(-self.iRate * self.timeToMaturity) * si.norm.cdf(-d2, 0.0, 1.0) - self.spotPrice * np.exp(-self.q * self.timeToMaturity) * si.norm.cdf(-d1, 0.0, 1.0))
            return self.optionPrice,'put',self.key
        
    
Option_Price = getOptionPrice('MSFT',120,0.5,0.025,0.2,0.25,option ='put').getOptionPrice()
print("The {} option price of {} is {}".format(Option_Price[1],Option_Price[2],Option_Price[0]))


''' sample output 
    The put option price of MSFT is 6.43
'''
