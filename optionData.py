from tkinter.filedialog import Open
from datetime import datetime
import pandas as pd
from optionCalculator import OptionCalculator
from spotPriceUtil import getSpotPriceUtil
class OptionData:
    def __init__(self, close_price, spot_price,strike_price, days_to_experiation, risk_free_rate=5.5, volatility=80, up = 5, down = -5, percentage_step = 0.5 ) -> None:
        self.close_price = close_price
        self.S = spot_price
        self.K = strike_price
        self.T = days_to_experiation
        self.r = risk_free_rate
        self.sigma = volatility
        self.up = up
        self.down = down
        self.percentage_step = percentage_step
        self.current_pct = (self.S - self.close_price)/self.close_price * 100
    
    # def getSpotPirce(self):
    #     number_of_spots = int((self.up - self.down)/self.percentage_step)
    #     spotPriceDf = pd.DataFrame(columns = ['spot price', 'percentage change'])
    #     # upperSpotPrice = self.close_price * (1 + self.up/100)
    #     lowerSpotPrice = self.close_price * (1 + self.down/100)
    #     # spotPriceDf = spotPriceDf.append({'spot price':upperSpotPrice, 'percentage change':self.up}, ignore_index=True)
    #     for n in range(number_of_spots):
    #         percentage = self.up - n * self.percentage_step
    #         spot_price = self.close_price*(1+ percentage/100) 
    #         # print('percent ', percentage)
    #         spotPriceDf = spotPriceDf.append({'spot price':spot_price, 'percentage change':percentage}, ignore_index = True)
    #     spotPriceDf = spotPriceDf.append({'spot price':lowerSpotPrice, 'percentage change':self.down}, ignore_index = True)
    #     return spotPriceDf

    def getSpotPrice(self):
        return getSpotPriceUtil(self.close_price, self.up, self.down, self.percentage_step)
        
    def getOptionPrices(self):
        spotPriceDf = self.getSpotPrice()
        optionPriceDf = pd.DataFrame(columns=['percentage', 'price','call', 'put', 'call pct change', 'put pct change'])
        spotOptionCalculator = OptionCalculator(self.S, self.K, self.T, self.r, self.sigma)
        spotCallPrice = spotOptionCalculator.bs_call()
        spotPutPrice = spotOptionCalculator.bs_put()
        optionPriceDf = optionPriceDf.append({'percentage':round(self.current_pct,2), 'price':round(self.S,2), 'call': round(spotCallPrice,2), 'put':round(spotPutPrice,2), 'call pct change':0, 'put pct change':0}, ignore_index=True)
        for (S,P) in spotPriceDf.values:
            optionCalculator = OptionCalculator(S, self.K, self.T, self.r, self.sigma)
            callPrice = optionCalculator.bs_call()
            putPrice = optionCalculator.bs_put()
            callPctChange = (callPrice - spotCallPrice)/spotCallPrice * 100
            putPctChange = (putPrice - spotPutPrice) / spotPutPrice * 100
            optionPriceDf = optionPriceDf.append({'percentage':round(P,2), 'price':round(S,2), 'call': round(callPrice,2), 'put': round(putPrice,2), 'call pct change':round(callPctChange,2), 'put pct change':round(putPctChange,2)}, ignore_index= True)
        return optionPriceDf

if __name__ == "__main__":
    starttime=datetime.now()
    stock_price = 20.94
    strike_price = 21
    date_to_expiration = 7
    risk_free_rate = 5.5
    volatility = 57.6
    optionData = OptionData(stock_price+1,stock_price,strike_price, date_to_expiration, risk_free_rate, volatility)
    spotPriceDf = optionData.getSpotPrice()
    # print(spotPriceDf)
    optionPriceDf = optionData.getOptionPrices()
    endtime=datetime.now()
    print(optionPriceDf)
    print("time used: ", endtime-starttime)