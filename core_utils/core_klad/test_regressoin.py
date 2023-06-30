from yahooquery import Ticker

symbols = "fb aapl amzn nflx goog"

tickers = Ticker(symbols)

# Retrieve each company's profile information
data = tickers.asset_profile
