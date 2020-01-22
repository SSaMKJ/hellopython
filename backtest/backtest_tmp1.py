# -*- coding: utf-8 -*-

from service.daily_data import DailyData
from service.market_cap import MarketCap
import backtrader as bt

marketCap = MarketCap()

cospi = marketCap.load(limit=100 * 2, market='COSPI')

daily = DailyData()

# 효성='004800'

cosDF = daily.get_daily('004800', end_date='2020-01-14')



class SmaCross(bt.Strategy): # bt.Strategy를 상속한 class로 생성해야 함.
    params = dict(
        pfast=20, # period for the fast moving average
        pslow=120 # period for the slow moving average
        )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
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
            size = int(self.broker.getcash() / close) # 최대 구매 가능 개수
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


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None

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
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(SmaCross)


cosDF.to_csv('csv_example')  #filling that buffer

import backtrader.feeds as btfeeds


class customCSV(btfeeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
    )

# Add the Data Feed to Cerebro
cerebro.adddata(customCSV(dataname='csv_example'))

# Set our desired cash start
cerebro.broker.setcash(10000000.0)

# Print out the starting conditions
seedMoney = cerebro.broker.getvalue()
print('Starting Portfolio Value: %.2f' % seedMoney)

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print(f'{cerebro.broker.getvalue()*100 / seedMoney}%')