# -*- coding: utf-8 -*-
from stockstats import StockDataFrame

from crawler.market_daily import MarketDaily
from service.decorators.decorators import *


class DailyData:

    @classmethod
    def get_daily(cls, code, start_date=None, end_date=None):

        df = MarketDaily(code, start_date, end_date)

        # add_mas(df)
        # add_RSI(df)
        # add_bollinger_band(df)
        # calMACD(df)
        # get_stochastic(df)
        # add_momentum(df)


        add_wr(df)
        return df
# https://pypi.org/project/stockstats/


def add_wr(df):
    print(df.columns)
    ddd = StockDataFrame.retype(df)
    print(df.columns)
    print(ddd.columns)
    wr_6 = ddd['wr_6']
    wr_10 = ddd['wr_10']
    df['wr_6'] = wr_6
    df['wr_10'] = wr_10
    print(df.columns)

dd = DailyData()
data = dd.get_daily('005930', '2019-01-28')
stock = StockDataFrame.retype(data)
print(stock.columns)
print(stock.tail(20))
print(stock['wr_10'].tail(20))
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also

    print(stock[['close', 'change','wr_6', 'wr_10']].tail(200))