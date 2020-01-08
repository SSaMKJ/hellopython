# -*- coding: utf-8 -*-
from crawler.market_cap import MarketCap
import json

file_name_market_cap = 'data/today-market-cap.txt'
MarketCap(file_name_market_cap)
with open(file_name_market_cap, 'r', encoding='UTF-8') as f:
    marketCap = eval(f.readlines()[0])


for i in range(201):
    code = marketCap[i]
    print(code)