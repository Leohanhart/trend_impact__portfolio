# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:58:20 2023

@author: Gebruiker
"""

import yfinance as yf
import pandas as pd

# Define the tickers for the US 10-year Treasury and the 7 biggest European 10-year Treasury bonds
us_ticker = "^TNX"
germany_ticker = "^DE10YB"
france_ticker = "^FR10YT"
italy_ticker = "^IT10YT"
spain_ticker = "^ES10YT"
netherlands_ticker = "^NL10YT"
belgium_ticker = "^BE10YT"
portugal_ticker = "^PT10YT"

# Download historical data for the tickers
us_data = yf.download(us_ticker, period="max")
germany_data = yf.download(germany_ticker, period="max")
france_data = yf.download(france_ticker, period="max")
italy_data = yf.download(italy_ticker, period="max")
spain_data = yf.download(spain_ticker, period="max")
netherlands_data = yf.download(netherlands_ticker, period="max")
belgium_data = yf.download(belgium_ticker, period="max")
portugal_data = yf.download(portugal_ticker, period="max")

# Merge the dataframes on the date index
merged_data = us_data.merge(
    germany_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    france_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    italy_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    spain_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    netherlands_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    belgium_data, how="inner", left_index=True, right_index=True
)
merged_data = merged_data.merge(
    portugal_data, how="inner", left_index=True, right_index=True
)

# Calculate the average yield of the European bonds
merged_data["euro_avg"] = merged_data.mean(axis=1)

# Calculate the yield spread as the difference between the US 10-year Treasury yield and the average yield of the European bonds
merged_data["yield_spread"] = merged_data["^TNX"] - merged_data["euro_avg"]

# Print the last 10 rows of the dataframe, which will show the most recent yield spread data
print(merged_data.tail(10))
