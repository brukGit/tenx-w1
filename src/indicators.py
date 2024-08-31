import talib
import pandas as pd

class TechnicalIndicators:
    """
    A class to apply technical analysis indicators using TA-Lib.

    Attributes:
    ----------
    data : dict
        A dictionary where the keys are stock tickers and values are DataFrames with stock data.

    Methods:
    -------
    calculate_moving_average(window=20):
        Calculates and adds the moving average (MA) to each DataFrame.
    
    calculate_rsi(period=14):
        Calculates and adds the Relative Strength Index (RSI) to each DataFrame.

    calculate_macd():
        Calculates and adds the MACD, MACD Signal, and MACD Histogram to each DataFrame.
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the TechnicalIndicators object.

        Parameters:
        ----------
        data : dict
            A dictionary where the keys are stock tickers and values are DataFrames with stock data.
        """
        self.data = data

    def calculate_moving_average(self, window=20):
        """
        Calculates the moving average (MA) and adds it to each stock's DataFrame.

        Parameters:
        ----------
        window : int, optional
            The window size for the moving average, by default 20.
        """
        for ticker, df in self.data.items():
            ma = talib.SMA(df['Close'], timeperiod=window)
            df['MA'] = ma[window-1:]  # Remove NaN values
            df['MA'].fillna(method='bfill', inplace=True)  # Backfill remaining NaNs

    def calculate_rsi(self, period=14):
        """
        Calculates the Relative Strength Index (RSI) and adds it to each stock's DataFrame.

        Parameters:
        ----------
        period : int, optional
            The time period for calculating RSI, by default 14.
        """
        for ticker, df in self.data.items():
            rsi = talib.RSI(df['Close'], timeperiod=period)
            df['RSI'] = rsi[period:]  # Remove NaN values
            df['RSI'].fillna(method='bfill', inplace=True)  # Backfill remaining NaNs

    def calculate_macd(self, fastperiod=12, slowperiod=26, signalperiod=9):
        """
        Calculates the MACD, MACD Signal, and MACD Histogram and adds them to each stock's DataFrame.
        """
        for ticker, df in self.data.items():
            macd, signal, hist = talib.MACD(df['Close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
            
            # Determine the index where MACD values start
            start_index = max(fastperiod, slowperiod) - 1
            
            df['MACD'] = macd[start_index:]
            df['MACD_signal'] = signal[start_index:]
            df['MACD_Histogram'] = hist[start_index:]
            
            # Backfill remaining NaNs
            df['MACD'].fillna(method='bfill', inplace=True)
            df['MACD_signal'].fillna(method='bfill', inplace=True)
            df['MACD_Histogram'].fillna(method='bfill', inplace=True)
