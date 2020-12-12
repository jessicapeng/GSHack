import pandas_datareader as pdr
import datetime
from gs_quant.data import Dataset, Fields

import json
import requests

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from gs_quant.session import GsSession, Environment

GsSession.use(client_id='c8a9707af9bc453e8f08f69eb44d1d0a',
    client_secret='e36e001a7ab7205c46d7e9d09794b46f1b019f0d71d5857c4bdf7681f2c24e6a',
    scopes=('read_product_data',))

start = datetime.date(2020, 6, 21)
end = datetime.date(2020, 12, 1)

sp500 = pdr.get_data_yahoo('VOO', start=start, end=end)

smallcap = pdr.get_data_yahoo('VB', start=start, end=end)
midcap = pdr.get_data_yahoo('VO', start=start, end=end)
largecap = pdr.get_data_yahoo('VV', start=start, end=end)

df = pd.DataFrame()
df['S&P500'] = sp500['Adj Close']
df['Small Cap'] = smallcap['Adj Close']
df['Mid Cap'] = midcap['Adj Close']
df['Large Cap'] = largecap['Adj Close']

graph = df.plot(y=['S&P500', 'Small Cap', 'Mid Cap', 'Large Cap'], figsize=(12, 8), lw=4, title="Adjusted Close Prices", grid=True)
graph.set_ylabel("Daily Adjusted Close Price")
graph.set_facecolor("#000000")

who_dataset = Dataset('COVID19_COUNTRY_DAILY_WHO')
data_frame = who_dataset.get_data(countryId='US', start=start, end=end)

ax = data_frame['totalConfirmed'].plot(grid=True, figsize=(12, 8), title="Total Confirmed Cases by WHO", lw=4)
# ax = data_frame.plot(grid=True, y=['totalConfirmed', 'totalFatalities'], figsize=(12, 8), title="Total Confirmed Cases and Fatalities by WHO", lw=4)
ax.set_ylabel("Daily Total Confirmed Cases")
ax.set_facecolor("#000000")  

