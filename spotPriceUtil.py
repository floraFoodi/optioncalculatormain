import pandas as pd
# def getSpotPriceUtil(close_price, up, down, percentage_step = 0.5):
#     number_of_spots = int((up - down)/percentage_step)
#     spotPriceDf = pd.DataFrame(columns = ['spot price', 'percentage change'])
#     # upperSpotPrice = self.close_price * (1 + self.up/100)
#     lowerSpotPrice = close_price * (1 + down/100)
#     # spotPriceDf = spotPriceDf.append({'spot price':upperSpotPrice, 'percentage change':self.up}, ignore_index=True)
#     for n in range(number_of_spots):
#         percentage = up - n * percentage_step
#         spot_price = close_price*(1+ percentage/100) 
#         # print('percent ', percentage)
#         spotPriceDf = spotPriceDf.append({'spot price':spot_price, 'percentage change':percentage}, ignore_index = True)
#     spotPriceDf = spotPriceDf.append({'spot price':lowerSpotPrice, 'percentage change':down}, ignore_index = True)
#     return spotPriceDf

def getSpotPriceUtil(spot_price, target_price, stop_price, atr, number_of_steps = 5):
    number_of_spots = number_of_steps * 2 + 3 # up and down the same number of steps, plus spot, target and stop prices
    spotPriceDf = pd.DataFrame(columns = ['spot price', 'percentage change'])
    # upperSpotPrice = self.close_price * (1 + self.up/100)
    upperSpotPrice = spot_price + number_of_steps * atr
    upper_percentage = ((upperSpotPrice-spot_price)/spot_price)*100
    target_percentage = ((target_price - spot_price)/spot_price)*100
    stop_percentage = ((stop_price - spot_price)/spot_price)*100
    spotPriceDf = spotPriceDf.append({'spot price': target_price, 'percentage change':target_percentage}, ignore_index = True)
    spotPriceDf = spotPriceDf.append({'spot price': stop_price, 'percentage change':stop_percentage}, ignore_index = True)
    # spotPriceDf = spotPriceDf.append({'spot price':upperSpotPrice, 'percentage change':upper_percentage}, ignore_index = True)

    for n in range(number_of_spots):
        spot_price_calc = upperSpotPrice - n * atr
        percentage = ((spot_price_calc - spot_price)/spot_price)*100
        # print('percent ', percentage)
        # prin(n, spot_price_calc)
        spotPriceDf = spotPriceDf.append({'spot price':spot_price_calc, 'percentage change':percentage}, ignore_index = True)
    return spotPriceDf