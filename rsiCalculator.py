from datetime import datetime
import pandas as pd

class RSICALCULATOR:
    def __init__(self, dataframe, period = 3) -> None:
        self.df = dataframe
        self.period = period
    
    def rsi(self):
        self.df['change'] = self.df['adjClose'].diff()
        # print(self.df)
        self.df['gain'] = self.df.change.mask(self.df.change < 0, 0.0)
        self.df['loss'] = -self.df.change.mask(self.df.change > 0, -0.0)
#Yahoo finance chart RSI calculation with the alpha 2.0/(n+1)
        self.df['avg_gain'] = self.df.gain.ewm(alpha=(1/self.period), adjust=False, min_periods=self.period).mean() 
        self.df['avg_loss'] = self.df.loss.ewm(alpha=(1/self.period), adjust=False, min_periods=self.period).mean()   
        self.df['rs'] = abs(self.df.avg_gain /self.df.avg_loss)
        self.df['rsi'] = 100 - (100 / (1+self.df.rs))
        # returnDf = self.df['rsi'].to_frame()
        returnDf = self.df['rsi']
        return returnDf

if __name__ == "__main__":
    starttime = datetime.now()
    df = pd.read_csv("/Users/floraqian/Downloads/AMD.csv")      
    YRSI = RSICALCULATOR(df)
    df = YRSI.rsi()
    # print(df)
    endtime = datetime.now()
    print("time used: ", endtime-starttime)
