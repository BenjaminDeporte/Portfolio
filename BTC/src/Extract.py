import numpy as np
import os
import matplotlib
# Prefer a non-interactive backend when running under debuggers or headless environments
matplotlib.use(os.environ.get('MPLBACKEND', 'QtAgg'))
# matplotlib.use('Qt5Agg')   # or 'QtAgg'/'Qt5Agg'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
import datetime
import time
from dotenv import dotenv_values
from tqdm import tqdm
from binance.client import Client
import argparse

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# CLI
# extract parameters
# - crypto: cryptocurrency to extract (default: BTCUSDT)
# - start_time: start time for data extraction (default: 2021-01-01 00:00:00)
# - end_time: end time for data extraction (default: now)
# - interval: data interval (default: 1 minute)
# - output: output file path (default: ./data/)
parser = argparse.ArgumentParser(description='Extract cryptocurrency data from Binance API.')
# No required positional argument — all flags are optional. Remove the accidental positional.
parser.add_argument("--crypto", type=str, default="BTCUSDT", help="Cryptocurrency to extract (default: BTCUSDT)")
parser.add_argument("--start_time", type=str, default="2021-01-01 00:00:00", help="Start time for data extraction (default: 2021-01-01 00:00:00)")
parser.add_argument("--end_time", type=str, default=None, help="End time for data extraction (default: now)")
parser.add_argument("--interval", type=str, default="1m", choices=['1m','5m','1h','1d'], help="Data interval (default: 1 minute)")
parser.add_argument("--output", type=str, default="output", help="Output file name (default: output)")
args = parser.parse_args()

print(f"Running with arguments: {args}")

# load Binance API keys ------------------------------------------------
filepath = "/home/benjamin/Folders_Python/Book/BTC/data/env/vars.env"
config = dotenv_values(filepath)

try:
    api_key = config['API_KEY']
    api_secret = config['API_SECRET']
    print(f'Key loading successful')
except KeyError:
    print("API key or secret not found in the environment file.")
    
client = Client(api_key, api_secret)

# extract data ---------------------------------------------------------
# define crypto to extract
if args.crypto is None:
    crypto = "BTCUSDT"
else:
    crypto = args.crypto

# Define custom start and end time
if args.start_time is None:
    start_time = datetime.datetime(2021, 1, 1, 0, 0, 0)
else:
    start_time = datetime.datetime.strptime(args.start_time, "%Y-%m-%d %H:%M:%S")

if args.end_time is None:
    end_time = datetime.datetime.now()
else:
    end_time = datetime.datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S")

time_signature = f"{crypto}-{start_time.year}-{start_time.month}-{start_time.day}" + f"-{end_time.year}-{end_time.month}-{end_time.day}" + f"-{args.interval}"

# interval
if args.interval is None:
    interval = Client.KLINE_INTERVAL_1MINUTE
else:
    interval = args.interval
    if interval == '1m':
        interval = Client.KLINE_INTERVAL_1MINUTE
    elif interval == '5m':
        interval = Client.KLINE_INTERVAL_5MINUTE
    elif interval == '1h':
        interval = Client.KLINE_INTERVAL_1HOUR
    elif interval == '1d':
        interval = Client.KLINE_INTERVAL_1DAY
        
# output
if args.output is None:
    output = "output"
else:
    output = args.output
outputfile = "/home/benjamin/Folders_Python/Book/BTC/data/extract/" + output + time_signature + ".csv"
    
# donne des nouvelles
print(f"Fetching data for {crypto} from {start_time} to {end_time} - interval: {args.interval}")

# récupère infos
klines = client.get_historical_klines(
        symbol=crypto, 
        interval=interval, 
        start_str=str(start_time), 
        end_str=str(end_time)
    )
    
# Convert the data into a pandas dataframe for easier manipulation
df = pd.DataFrame(
        klines, 
        columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
    )
columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
for col in tqdm(columns_to_convert):
    df[col] = df[col].astype(float)
    # Convert 'Open Time' and 'Close Time' to datetime format
    
df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
df['Close Time'] = pd.to_datetime(df['Close Time'], unit='ms')
# Use the Open Time as the DataFrame index so plots use dates on the x-axis
df.set_index('Open Time', inplace=True)
    
# save data to CSV
df.to_csv(outputfile, index=False)

# plot extracted data -------------------------------------------------
fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(20, 12), sharex=True)
df['Open'].plot(ax=ax[0], title='Open Price')
df['High'].plot(ax=ax[1], title='High Price')
df['Low'].plot(ax=ax[2], title='Low Price')
df['Close'].plot(ax=ax[3], title='Close Price')
for a in ax:
    a.set_ylabel('Price (USDT)')
    # draw grid below plotted lines and use a visible style
    a.set_axisbelow(True)
    a.grid(True, which='major', linestyle='--', linewidth=0.6, color='gray', alpha=0.7)
    # add minor ticks and a lighter minor grid for better readability
    a.minorticks_on()
    a.grid(True, which='minor', linestyle=':', linewidth=0.4, color='gray', alpha=0.4)
    a.xaxis.set_major_locator(mdates.AutoDateLocator())
    a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    a.tick_params(axis='x', rotation=45)

# Leave space at the top for the suptitle so it appears above ax[0]
plt.tight_layout(rect=(0, 0, 1, 0.95))
fig.suptitle(f'{crypto} Price Data', fontsize=16, y=0.98)

plt.show()