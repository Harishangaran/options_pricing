# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:45:52 2020

@author: harishangaran

PYTHON OPTION PRICE FOR NON-DIVIDEND PAYING STOCKS
"""

import yfinance as yf
import numpy as np
import scipy.stats as si

'''
The following script calculates European call and put option price
using the last close price from yahoo finance as the spot price.
The script is dynamic as it will request the latest price of the equity.

Just call the class and put or call method to get the option prices:
    call option price = getOptionPrice('equity',strickeprice,
                                       time to maturity in years,
                                       interest rate,sigma).callOption()
    
    eg: getOptionPrice('MSFT',150,0.5,0.05,0.25).callOption()
    
    put option price = getOptionPrice('equity',strickeprice,
                                       time to maturity in years,
                                       interest rate,sigma).putOption()
    
    eg: getOptionPrice('AAPL',180,0.5,0.05,0.25).putOption()

K: strike price
T: time to maturity in years
r: interest rate
sigma: volatility of underlying asset
'''


class getOptionPrice:
    def __init__(self,equitykey,K,T,r,sigma):
        self.key = equitykey
        self.strikePrice = K
        self.timeToMaturity = T
        self.iRate = r
        self.sigma = sigma
        self.callSpotPrice()
        self.callOption()
        self.putOption()
        
    def callSpotPrice(self):
        self.instrument = yf.Ticker(self.key)
        self.lastDayPrice = self.instrument.history(period='1d')
        self.spotPrice = self.lastDayPrice['Close']
        return self.spotPrice
    def callOption(self):
        d1 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate + 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        d2 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate - 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        self.call = (self.spotPrice * si.norm.cdf(d1, 0.0, 1.0) - self.strikePrice * np.exp(-self.iRate * self.timeToMaturity) * si.norm.cdf(d2, 0.0, 1.0))
        return self.call
    def putOption(self):
        d1 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate + 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        d2 = (np.log(self.spotPrice / self.strikePrice) + (self.iRate - 0.5 * self.sigma ** 2) * self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        self.put = (self.strikePrice * np.exp(-self.iRate * self.timeToMaturity) * si.norm.cdf(-d2, 0.0, 1.0) - self.spotPrice * si.norm.cdf(-d1, 0.0, 1.0))
        return self.put
        
    
current_Put_Option_Price = getOptionPrice('MSFT',100,0.5,0.025,0.25).putOption()
print('The current put option is {}'.format(current_Put_Option_Price))
