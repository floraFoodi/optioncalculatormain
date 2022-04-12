from numpy import DataSource
from pandas import DataFrame
from pandas_datareader import data
from datetime import date
class HISTORICALDATA:
    def __init__(self, stock_name=None, full_start_date = '2020-01-01', end_date = date.today()) -> None:
        self.api_key='726a59f0b7166631e4b0dd2fc3e0050999c8eb81'
        self.data_source = 'tiingo'
        self.full_start_date = full_start_date
        self.end_date = end_date
        if stock_name is not None:
            self.stock_name = stock_name
            print('symbol', stock_name)
        else:
            self.stock_name = self.question()
    def question(self):
        stock_name = input("Enter stock name: ")
        return stock_name
    def getDataDF(self) -> DataFrame:
        return data.DataReader(name=self.stock_name, data_source=self.data_source, start=self.full_start_date, end=self.end_date, api_key=self.api_key)

if __name__ =="__main__":
    HISTORICALDATA = HISTORICALDATA("COMP")
    df= HISTORICALDATA.getDataDF()
    df.to_csv("/Users/floraqian/Downloads/IXICtest.csv")