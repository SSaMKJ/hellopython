# -*- coding: utf-8 -*-
import os
import json

from crawler.market_daily import MarketDaily
from service.market_cap import MarketCap

companies = MarketCap().load(limit=1)
print(companies)

# file_name_market_cap = 'data/today-market-cap.txt'
# MarketCap(file_name_market_cap)
# with open(file_name_market_cap, 'r', encoding='UTF-8') as f:
#     marketCap = eval(f.readlines()[0])
#
#
# for i in range(201):
#     code = marketCap[i]
#     print(code)


df = MarketDaily('181710')


print(df.tail(2).index[0])
print(df.tail(2).to_json(orient='records'))