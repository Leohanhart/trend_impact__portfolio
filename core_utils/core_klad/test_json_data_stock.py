from core_scripts.stock_data_download import power_stock_object
import datetime


data = power_stock_object.power_stock_object(stock_ticker="CAR", periode_weekly = True)

previous_date = datetime.datetime.today() - datetime.timedelta(days=10000)
now_date = datetime.datetime.today()

print(data.stock_data.loc[previous_date:now_date])