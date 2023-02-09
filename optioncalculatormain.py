from email import header
from email.mime import base
import xlwings as xw
import pandas as pd
from optionData import OptionData
from rsiData import RSIData
from historicalData import HISTORICALDATA
from news import News



def getBaseParams(sheet,type):
    if type == 0:  #Call params
        return sheet.range('A2:D2').value
    else:
        return sheet.range('O2:R2').value
    
def getParmsDf(sheet,n):
    # rng = sheet.range((4, 6+7*n),(5, 10+7*n))
    rng = sheet.range((4, 1+7*n),(5, 5+7*n))
    print(rng.options(pd.DataFrame, header=1).value)
    return rng.options(pd.DataFrame, header=1).value

def writeOptions(sheet, n, df):
    clearForm(sheet, n)
    #start populate 6 columnns away from the first column
    # sheet.range((8, 6+(n*7))).options(index=False).value = df
    # print('write form')
    sheet.range((8, 1+(n*7))).options(index=False).value = df
def writeRSI(sheet, df):
    sheet.range((8,1)).expand().clear_contents()
    sheet.range((8, 1)).options(index=False).value = df
def clearForm(sheet, n):
    # print('clearing form')
    # sheet.range((8, 6+(n*7))).expand().clear_contents()
    sheet.range((8, 1+(n*7))).expand().clear_contents()
    
def populateOption(sheet, n, baseParams):
    (spotPrice, targetPrice, stopPrice, atr) = baseParams
    params = getParmsDf(sheet,n).values
    print(params)
    strikePrice = params[0,0]
    expirationDays = params[0,1]
    volatility = params[0,2]
    riskFreeRate = params[0,3]
    print(spotPrice, targetPrice, strikePrice, expirationDays, volatility, riskFreeRate)
    if riskFreeRate is not None:
        optionData = OptionData(spot_price=spotPrice, target_price=targetPrice, stop_price=stopPrice, atr=atr,strike_price=strikePrice, days_to_experiation=expirationDays, risk_free_rate=riskFreeRate, volatility=volatility)
    else:
        # optionData = OptionData(target_price=targetPrice, spot_price=spotPrice, strike_price=strikePrice, days_to_experiation=expirationDays, volatility=volatility, stop_price=stopPrice, atr=atr)
        optionData = OptionData(spot_price=spotPrice, target_price=targetPrice, stop_price=stopPrice, atr=atr,strike_price=strikePrice, days_to_experiation=expirationDays, volatility=volatility)
    print('start calculation')
    optionDf = optionData.getOptionPrices()
    # print(optionDf)
    print('getting ready')
    writeOptions(sheet, n, optionDf)
def populateRSI(sheet, df, baseParams):
    (spotPrice, closePrice, up, down) = baseParams
    rsiData = RSIData(df, close_price=closePrice, spot_price=spotPrice, up=up, down=down)
    df = rsiData.getCalculatedRSI()
    # print(df)
    writeRSI(sheet, df)
def writeNews(sheet,df):
    sheet.range((50,1)).expand().clear_contents()
    sheet.range((50,1)).options(index=False).value = df

def populateNews(sheet, ticker, period=1):
    news = News(ticker, period)
    df = news.getNews()
    writeNews(sheet,df)

def main():
    #Read Excel Book  
    wb = xw.Book.caller()
    #Read Ticker Symbol and decide whether to update the corresponding sheet based on the update flag. 1 = update, 0 = no-update
    stockListSheet = wb.sheets['StockList']
    stockDf = stockListSheet.range('StockListRange').options(pd.DataFrame, header=1).value
    stockDf.dropna(subset = ['Ticker'], inplace = True)
    print(stockDf)
    #Move to the sheet that needs to update and perform updates.
    for (T, update) in stockDf.values:
        if update == 1:
            print("udpate is true")
            try:
                sheet = wb.sheets[T]
                historicalDf = HISTORICALDATA(T).getDataDF()
                #calculate and populate call option section
                baseParams = getBaseParams(sheet,0)
                for n in range(2):
                    print("call option ",n)
                    populateOption(sheet, n, baseParams)
                #calculate and populate put option section
                baseParams = getBaseParams(sheet, 1)
                for n in range(2,4):
                    print("put option", n)
                    populateOption(sheet, n, baseParams)
            except Exception as e:
                print('ERROR', T, e)
                pass

if __name__ == "__main__":
    xw.Book("optioncalculatormain.xlsm").set_mock_caller()
    main()
