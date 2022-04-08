from email import header
from email.mime import base
import xlwings as xw
import pandas as pd
from optionData import OptionData
from rsiData import RSIData
from historicalData import HISTORICALDATA
def getBaseParams(sheet):
    return sheet.range('A2:E2').value
    
def getParmsDf(sheet,n):
    rng = sheet.range((4, 5+7*n),(5, 9+7*n))
    return rng.options(pd.DataFrame, header=1).value

def writeOptions(sheet, n, df):
    clearForm(sheet, n)
    sheet.range((8, 5+(n*7))).options(index=False).value = df

def writeRSI(sheet, df):
    sheet.range((8,1)).expand().clear_contents()
    sheet.range((8, 1)).options(index=False).value = df
def clearForm(sheet, n):
    # print('clearing form')
    sheet.range((8, 5+(n*7))).expand().clear_contents()
    
def populateOption(sheet, n, baseParams):
    (spotPrice, closePrice, up, down, numberOfOptions) = baseParams
    params = getParmsDf(sheet,n).values
    # print(params)
    strikePrice = params[0,0]
    expirationDays = params[0,1]
    volatility = params[0,2]
    riskFreeRate = params[0,3]
    # print(spotPrice, closePrice, up, down, strikePrice, expirationDays, volatility, riskFreeRate)
    if riskFreeRate is not None:
        optionData = OptionData(close_price=closePrice, spot_price=spotPrice, strike_price=strikePrice, days_to_experiation=expirationDays, risk_free_rate=riskFreeRate, volatility=volatility, up=up, down=down)
    else:
        optionData = OptionData(close_price=closePrice, spot_price=spotPrice, strike_price=strikePrice, days_to_experiation=expirationDays, volatility=volatility, up=up, down=down)
    optionDf = optionData.getOptionPrices()
    # print(optionDf)
    writeOptions(sheet, n, optionDf)
def populateRSI(sheet, df, baseParams):
    (spotPrice, closePrice, up, down, numberOfOptions) = baseParams
    rsiData = RSIData(df, close_price=closePrice, spot_price=spotPrice, up=up, down=down)
    df = rsiData.getCalculatedRSI()
    # print(df)
    writeRSI(sheet, df)
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
        try:
            sheet = wb.sheets[T]
            if update == 1:
                historicalDf = HISTORICALDATA(T).getDataDF()
                #write the last value of the historical data to ensure this number is the same as close price
                sheet.range((4,2)).value="RSI last price"
                sheet.range((5,2)).value=historicalDf.iloc[-1, historicalDf.columns.get_loc('adjClose')]
                baseParams = getBaseParams(sheet)
                numberOfOptions = int(baseParams[4])
                populateRSI(sheet,historicalDf, baseParams)
                print(numberOfOptions)
                for n in range(numberOfOptions):
                    print("option choice ",n)
                    populateOption(sheet, n, baseParams)
        except Exception as e:
            print('ERROR', T, e)
            pass

if __name__ == "__main__":
    xw.Book("optioncalculatormain.xlsm").set_mock_caller()
    main()
