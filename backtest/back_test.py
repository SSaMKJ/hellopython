# -*- coding: utf-8 -*-

import datetime
from service.daily_data import DailyData
import backtrader as bt

import backtrader.feeds as btfeeds
import os

def is_exist_file(file_name):
    if (os.path.isfile(file_name)):
        return True
    else:
        return False


def month_ago(month):
    dt_date = datetime.date.today() - datetime.timedelta(days=month * 30)

    return dt_date.strftime('%Y-%m-%d')


class BackTest():
    @classmethod
    def __init__(cls, stock_code, cache=10000000, date_str=None, isLogging=True):
        if date_str is None:
            today = datetime.date.today()
            cls.date_str = today.strftime('%Y-%m-%d')
        else :
            cls.date_str = date_str
        cls.stock_code = stock_code
        cls.strategy = SmaCross
        cls.cache = cache

    @classmethod
    def run(cls):
        csv_file_name = f'tmp_{cls.stock_code}_{cls.date_str}.csv'
        if not is_exist_file(csv_file_name):
            daily = DailyData()
            dailyDF = daily.get_daily(cls.stock_code, end_date=cls.date_str)
            month = month_ago(120)
            dailyDF.query('index>=%r' % month).to_csv(csv_file_name)


        # Create a cerebro entity
        cls.cerebro = bt.Cerebro()
        # Add a strategy
        cls.cerebro.addstrategy(cls.strategy)
        # Add the Data Feed to Cerebro
        cls.cerebro.adddata(customCSV(dataname=csv_file_name))

        # Set our desired cash start
        cls.cerebro.broker.setcash(cls.cache)
        # Run over everything
        cls.cerebro.run()

        return cls.cerebro.broker.getvalue()

    @classmethod
    def plot(cls):
        cls.cerebro.plot()

    @classmethod
    def set_strategy(cls, strategy):
        cls.strategy = strategy


class customCSV(btfeeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('change', 6),
        ('gold_cross', -1),
    )




class SmaCross(bt.Strategy): # bt.Strategy를 상속한 class로 생성해야 함.
    params = dict(
        pfast=20, # period for the fast moving average
        pslow=120 # period for the slow moving average
        )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        if False:
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast) # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow) # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2) # crossover signal

        # To keep track of pending orders
        self.order = None

        self.buy_price = 0.0
        self.max_price = 0.0

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        # print(f'order = {self.order}')
        close = self.data.close[0]  # 종가 값
        self.max_price = max(self.max_price, close)
        if self.order:
            return

        if self.crossover > 0: # if fast crosses slow to the upside
            close = self.data.close[0] # 종가 값
            size = int(self.broker.getcash() / close) - 1# 최대 구매 가능 개수
            if size > 0:
                self.log(f'try buy cash[{self.broker.getcash()}], size=[{size}]')
                self.order =self.buy(size=size) # 매수 size = 구매 개수 설정
                self.max_price = close
                self.buy_price = close
        else :
            close = self.data.close[0]


            if self.buy_price > 0.0 and (close - self.buy_price) * 100 / self.buy_price < -3:
                sizer = self.broker.getposition(data=self.datas[0]).size
                self.order =self.sell(size=sizer) # 매도
                self.buy_price = 0
                self.max_price = 0

            elif self.buy_price > 0.0 and (close - self.buy_price) * 100 / self.buy_price > 10:
                sizer = self.broker.getposition(data=self.datas[0]).size
                self.order =self.sell(size=sizer) # 매도
                self.buy_price = 0
                self.max_price = 0
            elif self.buy_price > 0.0 and (close - self.max_price) * 100 / self.max_price < -5:
                sizer = self.broker.getposition(data=self.datas[0]).size
                self.order =self.sell(size=sizer) # 매도
                self.buy_price = 0
                self.max_price = 0
            # elif self.crossover < 0:
            #     sizer = self.broker.getposition(data=self.datas[0]).size
            #     self.order = self.sell(size=sizer)  # 매도
            #     self.buy_price = 0
            #     self.max_price = 0

