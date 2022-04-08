from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame

class OptionCalculator:
    def __init__(self, spot_price, strike_price, days_to_experiation, risk_free_rate=5.5, volatility=50) -> None:
        self.S = spot_price
        self.K = strike_price
        self.T = days_to_experiation/365
        self.r = risk_free_rate/100
        self.sigma = volatility/100
    def d1(self):
        return(log(self.S/self.K)+(self.r+self.sigma**2/2.)*self.T)/(self.sigma*sqrt(self.T))
    def d2(self):
        return self.d1()-self.sigma*sqrt(self.T)
    def bs_call(self):
        return self.S*norm.cdf(self.d1())-self.K*exp(-self.r*self.T)*norm.cdf(self.d2())
    def bs_put(self):
        return self.K*exp(-self.r*self.T)-self.S+self.bs_call()
    def call_delta(self):
        return norm.cdf(self.d1())
    def call_gamma(self):
        return norm.pdf(self.d1())/(self.S*self.sigma*sqrt(self.T))
    def call_vega(self):
        return 0.01*(self.S*norm.pdf(self.d1())*sqrt(self.T))
    def call_theta(self):
        return 0.01*(-(self.S*norm.pdf(self.d1())*self.sigma)/(2*sqrt(self.T)) - self.r*self.K*exp(-self.r*self.T)*norm.cdf(self.d2()))
    def call_rho(self):
        return 0.01*(self.K*self.T*exp(-self.r*self.T)*norm.cdf(self.d2()))
        
    def put_delta(self):
        return -norm.cdf(-self.d1())
    def put_gamma(self):
        return norm.pdf(self.d1())/(self.S*self.sigma*sqrt(self.T))
    def put_vega(self):
        return 0.01*(self.S*norm.pdf(self.d1())*sqrt(self.T))
    def put_theta(self):
        return 0.01*(-(self.S*norm.pdf(self.d1())*self.sigma)/(2*sqrt(self.T)) + self.r*self.K*exp(-self.r*self.T)*norm.cdf(-self.d2()))
    def put_rho(self):
        return 0.01*(-self.K*self.T*exp(-self.r*self.T)*norm.cdf(-self.d2()))

if __name__ == "__main__":
    stock_price = 20.94
    strike_price = 21
    date_to_expiration = 7
    risk_free_rate = 5.5
    volatility = 57.6
    calculator = OptionCalculator(stock_price, strike_price, date_to_expiration, risk_free_rate, volatility)

    print('d1: ', calculator.d1())
    print('d2', calculator.d2())

    print('The call Option Price is: ', calculator.bs_call())
    print('The Put option price is: ', calculator.bs_put())

    print("call greeks ", "delta ", calculator.call_delta())
    print("call greeks ", "gamma ", calculator.call_gamma())
    print("call greeks ", "vega ", calculator.call_vega())
    print("call greeks ", "theta ", calculator.call_theta())
    print("call greeks ", "rho ", calculator.call_rho())

    print("put greeks ", "delta ", calculator.put_delta())
    print("put greeks ", "gamma ", calculator.put_gamma())
    print("put greeks ", "vega ", calculator.put_vega())
    print("put greeks ", "theta ", calculator.put_theta())
    print("put greeks ", "rho ", calculator.put_rho())
