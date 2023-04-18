import tradingeconomics as te
import pandas as pd



te.login('guest:guest')

# Specify the country and indicator
country = 'united states'
indicator = 'gdp'

# Retrieve the historical data
data = te.getHistoricalData(country=country, indicator=indicator, output_type='df')

# Print the first 5 rows of the dataframe
print(data.head())

# Logout
te.logout()






























