import pandas as pd
def getSpotPriceUtil(close_price, up, down, percentage_step = 0.5):
    number_of_spots = int((up - down)/percentage_step)
    spotPriceDf = pd.DataFrame(columns = ['spot price', 'percentage change'])
    # upperSpotPrice = self.close_price * (1 + self.up/100)
    lowerSpotPrice = close_price * (1 + down/100)
    # spotPriceDf = spotPriceDf.append({'spot price':upperSpotPrice, 'percentage change':self.up}, ignore_index=True)
    for n in range(number_of_spots):
        percentage = up - n * percentage_step
        spot_price = close_price*(1+ percentage/100) 
        # print('percent ', percentage)
        spotPriceDf = spotPriceDf.append({'spot price':spot_price, 'percentage change':percentage}, ignore_index = True)
    spotPriceDf = spotPriceDf.append({'spot price':lowerSpotPrice, 'percentage change':down}, ignore_index = True)
    return spotPriceDf