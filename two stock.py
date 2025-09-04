import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def compare_stocks(ticker1, ticker2, start_date='2023-01-01', end_date=None):
    """
    Compares two stocks based on their historical closing prices.

    Args:
        ticker1 (str): The ticker symbol of the first stock.
        ticker2 (str): The ticker symbol of the second stock.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.
                        If None, data will be fetched up to the most recent day.
    """
    try:
        # Download historical data for the two stocks
        stock1_data = yf.download(ticker1, start=start_date, end=end_date)
        stock2_data = yf.download(ticker2, start=start_date, end=end_date)

        if stock1_data.empty or stock2_data.empty:
            print("Could not retrieve data for one or both tickers. Please check the symbols.")
            return

        # --- 1. Price Performance Comparison (Normalized) ---
        # Normalize the closing prices to see the performance over time starting from the same baseline.
        normalized_stock1 = (stock1_data['Close'] / stock1_data['Close'][0]) * 100
        normalized_stock2 = (stock2_data['Close'] / stock2_data['Close'][0]) * 100

        plt.figure(figsize=(14, 7))
        plt.plot(normalized_stock1, label=f'{ticker1} Normalized Price')
        plt.plot(normalized_stock2, label=f'{ticker2} Normalized Price')
        plt.title(f'Stock Price Performance: {ticker1} vs {ticker2}')
        plt.xlabel('Date')
        plt.ylabel('Normalized Price (Start = 100)')
        plt.legend()
        plt.grid(True)
        plt.show()

        # --- 2. Key Performance Metrics ---
        # Calculate daily returns
        stock1_returns = stock1_data['Close'].pct_change().dropna()
        stock2_returns = stock2_data['Close'].pct_change().dropna()

        # Calculate total return
        total_return_stock1 = (stock1_data['Close'][-1] - stock1_data['Close'][0]) / stock1_data['Close'][0]
        total_return_stock2 = (stock2_data['Close'][-1] - stock2_data['Close'][0]) / stock2_data['Close'][0]

        # Calculate volatility (standard deviation of daily returns)
        volatility_stock1 = stock1_returns.std()
        volatility_stock2 = stock2_returns.std()

        print("\n--- Key Performance Metrics ---")
        print(f"Period: {start_date} to {end_date if end_date else 'Today'}")
        print("\n" + "="*40)
        print(f"Ticker: {ticker1}")
        print(f"Total Return: {total_return_stock1:.2%}")
        print(f"Volatility (Daily): {volatility_stock1:.4f}")
        print("="*40)
        print(f"Ticker: {ticker2}")
        print(f"Total Return: {total_return_stock2:.2%}")
        print(f"Volatility (Daily): {volatility_stock2:.4f}")
        print("="*40)

        # --- 3. Correlation ---
        returns_df = pd.DataFrame({ticker1: stock1_returns, ticker2: stock2_returns})
        correlation = returns_df.corr().iloc[0, 1]
        print(f"\nCorrelation between {ticker1} and {ticker2}: {correlation:.4f}")
        print("A value close to 1 means the stocks move in the same direction.")
        print("A value close to -1 means they move in opposite directions.")
        print("A value close to 0 means they have little to no linear relationship.")


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # --- USER INPUT ---
    # You can change the stock tickers and the date range here
    stock_ticker_1 = 'GOOGL'  # Example: Google
    stock_ticker_2 = 'MSFT'   # Example: Microsoft
    start = '2024-01-01'
    end = '2024-09-01'

    compare_stocks(stock_ticker_1, stock_ticker_2, start_date=start, end_date=end)
