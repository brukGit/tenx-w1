import pynance as pn
import numpy as np
import pandas as pd 

class FinancialMetrics:
    """
    A class to calculate financial metrics using PyNance.

    Attributes:
    ----------
    data : dict
        A dictionary where the keys are stock tickers and values are DataFrames with stock data.

    Methods:
    -------
    calculate_sharpe_ratio(risk_free_rate=0.0):
        Calculates the Sharpe Ratio for each stock and returns it as a dictionary.

    calculate_volatility(period=252):
        Calculates the volatility for each stock and returns it as a dictionary.
    """

    def __init__(self, data):
        """
        Constructs all the necessary attributes for the FinancialMetrics object.

        Parameters:
        ----------
        data : dict
            A dictionary where the keys are stock tickers and values are DataFrames with stock data.
        """
        self.data = data

    def calculate_sharpe_ratio(self, risk_free_rate=0.0):
        """
        Calculates the Sharpe Ratio for each stock.

        Parameters:
        ----------
        risk_free_rate : float, optional
            The risk-free rate to be used in the Sharpe Ratio calculation, by default 0.0.

        Returns:
        -------
        dict
            A dictionary where the keys are stock tickers and values are the Sharpe Ratios.
        """
        sharpe_ratios = {}
        for ticker, df in self.data.items():
            returns = df['Close'].pct_change().dropna()          
            # If we can't find the sharpe_ratio function, let's implement it ourselves
            excess_returns = returns - risk_free_rate
            sharpe_ratio = excess_returns.mean() / excess_returns.std()
            
            sharpe_ratios[ticker] = sharpe_ratio
        return sharpe_ratios

    def calculate_volatility(self, period=252):
        """
        Calculates the volatility for each stock based on a rolling window.

        Parameters:
        ----------
        period : int, optional
            The number of trading days to consider for the rolling window, by default 252.

        Returns:
        -------
        dict
            A dictionary where the keys are stock tickers and values are the calculated volatilities.
        """
        volatilities = {}
        for ticker, df in self.data.items():
            returns = df['Close'].pct_change().dropna()
            volatilities[ticker] = returns.rolling(window=period).std().iloc[-1]
        return volatilities
    
    def calculate_beta(self, market_returns):
        """
        Calculate the Beta of each stock relative to the market.

        The Beta coefficient measures the volatility of a stock in relation to the overall market. 
        Parameters:
            market_returns (pd.Series): A Pandas Series representing the market returns with dates as the index.

        Returns:
            dict: A dictionary where keys are stock tickers and values are their respective Beta coefficients.
        """

        betas = {}
        for ticker, df in self.data.items():
            # Ensure 'Date' is in the correct datetime format and set as the index
            # df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
            # df.set_index('Date', inplace=True)
            
            stock_returns = df['Close'].pct_change().dropna()

            # Ensure market_returns is in the same datetime format
            # market_returns.index = pd.to_datetime(market_returns.index).tz_localize(None)
            
            # Align the stock returns with market returns
            aligned_stock_returns, aligned_market_returns = stock_returns.align(market_returns, join='inner')
            
           
            # Calculate covariance and market variance
            covariance = np.cov(aligned_stock_returns, aligned_market_returns)[0][1]
            market_variance = np.var(aligned_market_returns)
            
            if market_variance == 0:
                beta = np.nan  # Market variance is zero, beta is undefined
                print(f"Warning: Market variance is zero for {ticker}. Beta set to NaN.")
            else:
                beta = covariance / market_variance
            
            betas[ticker] = beta
            
        return betas
