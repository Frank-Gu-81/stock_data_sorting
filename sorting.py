import pandas as pd
import numpy as np
from tables import Col

diff = pd.DataFrame(columns = ['symbol', 'exchange'])
diff = diff.to_csv('difference.csv', index = False)

yahoo = pd.read_csv('generic.csv')
yahoo.rename(columns = {'Ticker':'symbol', 'Exchange':'exchange'}, inplace = True)
# print(yahoo)
yahoo_stock = yahoo[yahoo['Type']=='S']
# print(yahoo_stock.shape)
# print(set(yahoo_stock['exchange']))
guru = pd.read_csv('concat.csv')
print(guru.shape)
yahoo_stock = yahoo_stock.reset_index()

for i in range(len(yahoo_stock)):
    if '.' in yahoo_stock.loc[i,'symbol']:
        yahoo_stock.at[i,'symbol']= yahoo_stock.loc[i,'symbol'].split('.')[0]
    if '-' in yahoo_stock.loc[i,'symbol']:
        yahoo_stock.at[i,'symbol']= yahoo_stock.at[i,'symbol'].replace('-','.')
result= yahoo_stock.merge(guru, how='inner', on='symbol')
print(result.shape)

# sort the result by symbol(tickers) in an alphabetical order so that it is easier to compare
guru_sorted_df = guru.sort_values(by=["symbol"], ascending=True)
yahoo_sorted_df = yahoo_stock.sort_values(by=["symbol"], ascending=True)
guru_sorted_csv = guru_sorted_df.to_csv('guru_sorted.csv', index = False) #symbols are in the first column: index = 0
yahoo_sorted_csv = yahoo_sorted_df.to_csv('yahoo_sorted.csv', index = False) #symbols are in the second column: index = 1

#-------------------------------acquire difference--------------------------------#

with open('yahoo_sorted.csv') as yahoo_info:
    check_set = set([row.split(',')[1].strip().upper() for row in yahoo_info])
    # check_set = set([row.strip()[0].upper() for row in yahoo_info])

with open('guru_sorted.csv', 'r') as in_file, open('difference.csv', 'w') as out_file:
    for line in in_file:
        if line.split(',')[0].strip().upper() not in check_set:
        # if line.strip()[0].upper() not in check_set:
            out_file.write(line)

diff_size = pd.read_csv('difference.csv')
print(diff_size.shape)