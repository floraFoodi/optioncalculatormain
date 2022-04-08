import pandas as pd
from spotPriceUtil import getSpotPriceUtil
from datetime import datetime
from rsiCalculator import RSICALCULATOR
class RSIData:
    def __init__(self,df, close_price, spot_price, up= 5, down = -5, percentage_step=0.5) -> None:
       self.df = df
       self.close_price = close_price
       self.S = spot_price
       self.up = up
       self.down = down
       self.percentage_step = percentage_step
    def getSpotPrice(self):
        return getSpotPriceUtil(self.close_price, self.up, self.down, self.percentage_step)
    
    def updateDataframe(self, spot_price):
        df = self.df.append(self.df.iloc[-1], ignore_index=True)
        df.iloc[-1, df.columns.get_loc('adjClose')] = spot_price
        # print(df.iloc[-5])
        return df

    def getLastRSI(self, df):
        return RSICALCULATOR(df).rsi().iloc[-1].item()

    def getCalculatedRSI(self):
        rsiDf = pd.DataFrame(columns=['percentage', 'price','rsi'])
        spotPercentage = (self.S - self.close_price)/self.close_price * 100
        spotDf = self.updateDataframe(self.S)
        spotRSI = self.getLastRSI(spotDf)
        rsiDf = rsiDf.append({'percentage': round(spotPercentage, 2), 'price':round(self.S, 2), 'rsi': round(spotRSI,2)}, ignore_index=True)
        spotPriceDf = self.getSpotPrice()
        # print(spotPriceDf)
        for (S,P) in spotPriceDf.values:
            updatedDf = self.updateDataframe(S)
            calculatedRSI = self.getLastRSI(updatedDf)
            rsiDf = rsiDf.append({'percentage': round(P, 2), 'price':round(S, 2), 'rsi': round(calculatedRSI,2)}, ignore_index=True)
        return rsiDf

if __name__ == "__main__":
    df = pd.read_csv("/Users/floraqian/Downloads/AALtest.csv")
    starttime=datetime.now()
    stock_price = 20.94
    strike_price = 21
    date_to_expiration = 7
    risk_free_rate = 5.5
    volatility = 57.6   
    RSIData = RSIData(df, stock_price+1, stock_price)  
    # df = RSIData.updateDataframe(stock_price+1)
    # print(df)
    # spotPriceDf = RSIData.getLastRSI(df)
    # print(spotPriceDf)
    rsiDf = RSIData.getCalculatedRSI()
    print(rsiDf)