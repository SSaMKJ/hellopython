# -*- coding: utf-8 -*-
from backtest.back_test import BackTest

import backtrader as bt

from backtest.starategies.TestStrategy import *


print('---')


from service.market_cap import MarketCap

def gethering_codes():
    limits = [300, 100]
    markets = ['COSPI', 'COSDAK']

    marketCap = MarketCap()
    stocks = []
    for i in range(len(markets)):
        stocks_info = marketCap.load(limit=limits[i], market=markets[i])

        for stock in stocks_info:
            # print(cos)
            try:
                per = float(stock['PER'])
            except Exception:
                continue

            if per < 0:
                continue
            stocks.append({'code': stock['code'], 'name': stock['name'], 'market': markets[i]})
    return stocks

sum_rate = []

bigger_than=0
lesser_than=0
for stock in gethering_codes():
    code = stock['code']
    back_test = BackTest(code, date_str='2020-01-14', isLogging=False)
    back_test.set_strategy(TestStrategy)
    rate = back_test.run() * 100 / 10000000
    print(f'{stock["name"]}={rate}%')
    sum_rate.append(rate)
    if rate > 100.0:
        bigger_than+=1
    else:
        lesser_than+=1

print(f'over 100 = {bigger_than}, under... = {lesser_than}')
print(sum(sum_rate)/len(sum_rate))