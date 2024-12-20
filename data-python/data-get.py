import yfinance as yf
import os, contextlib

offset = 0
limit = 20000
period = 'max' 

import pandas as pd

data = pd.read_csv("http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt", sep='|')
data_clean = data[data['Test Issue'] == 'N']
symbols = data_clean['NASDAQ Symbol'].tolist()
print('total number of symbols traded = {}'.format(len(symbols)))

if not os.path.exists('hist'):
    os.mkdir('hist')

limit = limit if limit else len(symbols)
end = min(offset + limit, len(symbols))
is_valid = [False] * len(symbols)
# force silencing of verbose API
with open(os.devnull, 'w') as devnull:
    with contextlib.redirect_stdout(devnull):
        try:
            for i in range(offset, end):
                s = symbols[i]
                data = yf.download(s, period=period)
                if len(data.index) == 0:
                    continue

                is_valid[i] = True
                data.to_csv('stock-data-pipeline/db-python/hist/{}.csv'.format(s))
        except:
            pass

print('Total number of valid symbols downloaded = {}'.format(sum(is_valid)))

valid_data = data_clean[is_valid]
valid_data.to_csv('symbols_valid_meta.csv', index=False)
