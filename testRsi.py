import typing
import pandas as pd
import pandas_ta as ta
def wilders_rsi(data: typing.List[float or int], window_length: int,
                use_rounding: bool = True) -> typing.List[typing.Any]:
    """
    A manual implementation of Wells Wilder's RSI calculation as outlined in
    his 1978 book "New Concepts in Technical Trading Systems" which makes
    use of the α-1 Wilder Smoothing Method of calculating the average
    gains and losses across trading periods.

    @author: https://github.com/alphazwest

    Args:
        data: List[float or int] - a collection of floating point values
        window_length: int-  the number of previous periods used for RSI calculation
        use_rounding: bool - option to round calculations to the nearest 2 decimal places
    Returns:
        A list object with len(data) + 1 members where the first is a header as such:
             ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    """

    # Define a rounding function based on argument
    do_round = lambda x: round(x, 2) if use_rounding else x  # noqa: E731

    # Define containers
    gains: typing.List[float]       = []
    losses: typing.List[float]      = []
    window: typing.List[float]      = []

    # Define convenience variables
    prev_avg_gain: float or None    = None
    prev_avg_loss: float or None    = None

    # Define output container with header
    output: typing.List[typing.Any] = [
        ['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']
    ]
    for i, price in enumerate(data):

        # Skip first row but remember price
        if i == 0:
            window.append(price)
            output.append([i+1, price, 0, 0, 0, 0, 0])
            continue

        # Calculate price difference with previous period
        # difference = do_round(wilder_data[i] - wilder_data[i - 1])
        difference = do_round(data[i] - data[i - 1])

        # Record positive differences as gains, negative as losses
        if difference > 0:
            gain = difference
            loss = 0
        elif difference < 0:
            gain = 0
            loss = abs(difference)
        else:
            gain = 0
            loss = 0
        gains.append(gain)
        losses.append(loss)

        # Don't calculate averages until n-periods data available
        if i < window_length:
            window.append(price)
            output.append([i+1, price, gain, loss, 0, 0, 0])
            continue

        # Calculate Average for first gain as SMA
        if i == window_length:
            avg_gain = sum(gains) / len(gains)
            avg_loss = sum(losses) / len(losses)

        # Use WSM after initial window-length period
        else:
            avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
            avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

        # Round for precision
        avg_gain = do_round(avg_gain)
        avg_loss = do_round(avg_loss)

        # Keep in memory
        prev_avg_gain = avg_gain
        prev_avg_loss = avg_loss

        # Calculate RS
        rs = do_round(avg_gain / avg_loss)

        # Calculate RSI
        rsi = do_round(100 - (100 / (1 + rs)))

        # Remove oldest values
        window.append(price)
        window.pop(0)
        gains.pop(0)
        losses.pop(0)

        # Save Data
        output.append([i+1, price, gain, loss, avg_gain, avg_loss, rsi])

    return output


def pandas_rsi(df: pd.DataFrame, window_length: int = 14, output: str = None, price: str = 'Close'):
    """
    An implementation of Wells Wilder's RSI calculation as outlined in
    his 1978 book "New Concepts in Technical Trading Systems" which makes
    use of the α-1 Wilder Smoothing Method of calculating the average
    gains and losses across trading periods and the Pandas library.

    @author: https://github.com/alphazwest
    Args:
        df: pandas.DataFrame - a Pandas Dataframe object
        window_length: int - the period over which the RSI is calculated. Default is 14
        output: str or None - optional output path to save data as CSV
        price: str - the column name from which the RSI values are calcuated. Default is 'Close'

    Returns:
        DataFrame object with columns as such, where xxx denotes an inconsequential
        name of the provided first column:
            ['xxx', 'diff', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rs', 'rsi']
    """
    # Calculate Price Differences using the column specified as price.
    df['diff'] = df['close'].diff(1)

    # Calculate Avg. Gains/Losses
    df['gain'] = df['diff'].clip(lower=0).round(2)
    df['loss'] = df['diff'].clip(upper=0).abs().round(2)

    # Get initial Averages
    df['avg_gain'] = df['gain'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]
    df['avg_loss'] = df['loss'].rolling(window=window_length, min_periods=window_length).mean()[:window_length+1]

    # Calculate Average Gains
    for i, row in enumerate(df['avg_gain'].iloc[window_length+1:]):
        df['avg_gain'].iloc[i + window_length + 1] =\
            (df['avg_gain'].iloc[i + window_length] *
             (window_length - 1) +
             df['gain'].iloc[i + window_length + 1])\
            / window_length

    # Calculate Average Losses
    for i, row in enumerate(df['avg_loss'].iloc[window_length+1:]):
        df['avg_loss'].iloc[i + window_length + 1] =\
            (df['avg_loss'].iloc[i + window_length] *
             (window_length - 1) +
             df['loss'].iloc[i + window_length + 1])\
            / window_length

    # Calculate RS Values
    df['rs'] = df['avg_gain'] / df['avg_loss']

    # Calculate RSI
    df['rsi'] = 100 - (100 / (1.0 + df['rs']))

    # Save if specified
    if output is not None:
        df.to_csv(output)

    return df

def rsi(df, n):
    df['change'] = df['Close'].diff()
    df['gain'] = df.change.mask(df.change < 0, 0.0)
    df['loss'] = df.change.mask(df.change > 0, 0.0)
#Yahoo finance chart RSI calculation with the alpha 2.0/(n+1)
    df['avg_gain'] = df.gain.ewm(alpha=(1/n), adjust=False, min_periods=n).mean() 
    df['avg_loss'] = df.loss.ewm(alpha=(1/n), adjust=False, min_periods=n).mean()   
    # df['avg_gain'] = df.gain.rolling(n).mean()
    # df['avg_loss'] = df.loss.rolling(n).mean()    
 
    # df['avg_gain'] = df.gain.ewm(com=2, adjust=False).mean() 
    # df['avg_loss'] = df.loss.ewm(com=2, adjust=False).mean()
    df['rs'] = abs(df.avg_gain /df.avg_loss)
    df['rsi'] = 100.0 - (100.0 / (1.0+df.rs))
    print(df)
    return df
# data = [16.95, 17.15, 17.83, 17.56, 16.70, 18.10, 17.60, 16.85]

# output = wilders_rsi(data=data, window_length=3)

# print(output)s

# pdData = pd.DataFrame({'period':[1,2, 3,4,5,6,7,8],'close':[16.95, 17.15, 17.83, 17.56, 16.70, 18.10, 17.60, 16.85]})
# pdOutput = pandas_rsi(pdData,3,price='close')
# print(pdOutput)

# pdData = pdData.set_index(['period'])

# taOutput = ta.rsi(pdData['close'], 3)

# print(taOutput)
df = pd.read_csv("/Users/floraqian/Downloads/AMD.csv")
print(df.head)
output = rsi(df, 3)
output.to_csv("/Users/floraqian/Downloads/amd_rsi_alpha_1_n_false.csv")
print(output)