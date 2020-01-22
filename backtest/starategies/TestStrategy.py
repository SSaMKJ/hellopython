# -*- coding: utf-8 -*-

import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        return
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None
        self.max_price = 0.0
        self.buy_price = 0.0

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
                    close = self.data.close[0]  # 종가 값
                    size = int(self.broker.getcash() / close) - 1  # 최대 구매 가능 개수
                    if size > 0:
                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy(size=size)
                        self.max_price = close
                        self.buy_price = close

        else:
            close = self.data.close[0]

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                sizer = self.broker.getposition(data=self.datas[0]).size
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=sizer)
                self.buy_price = 0
                self.max_price = 0
            #
            # el
            # if self.buy_price > 0.0 and (close - self.buy_price) * 100 / self.buy_price < -3:
            #     sizer = self.broker.getposition(data=self.datas[0]).size
            #     self.order =self.sell(size=sizer) # 매도
            #     self.buy_price = 0
            #     self.max_price = 0
            #
            # elif self.buy_price > 0.0 and (close - self.buy_price) * 100 / self.buy_price > 10:
            #     sizer = self.broker.getposition(data=self.datas[0]).size
            #     self.order =self.sell(size=sizer) # 매도
            #     self.buy_price = 0
            #     self.max_price = 0
            # elif self.buy_price > 0.0 and (close - self.max_price) * 100 / self.max_price < -5:
            #     sizer = self.broker.getposition(data=self.datas[0]).size
            #     self.order =self.sell(size=sizer) # 매도
            #     self.buy_price = 0
            #     self.max_price = 0

