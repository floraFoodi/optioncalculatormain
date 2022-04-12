from curses import raw
import requests
import pandas as pd
from datetime import date, datetime, timedelta
class News:
    def __init__(self, stock_name=None, period = 1) -> None:
        self.api_key='726a59f0b7166631e4b0dd2fc3e0050999c8eb81'
        self.url = "https://api.tiingo.com/tiingo/news?token="
        self.stock_name = stock_name
        self.period = period
    def getRawNews(self):
        headers = {'Content-Type': 'application/json'}
        requestResponse = requests.get(self.url+self.api_key+"&"+"tickers="+self.stock_name, headers=headers)
        # print(requestResponse.json())
        df = pd.DataFrame(requestResponse.json())
        # print(df.head())
        return df

    def convertTime(self,x):
        dtFormat = '%Y-%m-%dT%H:%M:%SZ'
        dtFormatWithNS = '%Y-%m-%dT%H:%M:%S.%fZ'
        try: 
            return pd.to_datetime(x, format=dtFormat)
        except:
            return pd.to_datetime(x, format=dtFormatWithNS)
        
    def getNews(self):
        rawDf = self.getRawNews()
        dt = datetime.combine(datetime.today() - timedelta(days=self.period), datetime.min.time())
        rawDf['publishedDate'] = rawDf['publishedDate'].apply(lambda x: self.convertTime(x))
        df = rawDf[rawDf['publishedDate'] >= dt][['publishedDate','description', 'url']]
        return df

if __name__ == "__main__":
    news = News('PLUG')
    # news.getNews()
    news.getRawNews().to_csv("/Users/floraqian/Downloads/plugnewsraw.csv")      
     
    