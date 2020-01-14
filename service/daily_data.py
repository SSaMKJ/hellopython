# -*- coding: utf-8 -*-

from crawler.market_daily import MarketDaily

class DailyData:

    @classmethod
    def get_daily(cls, code, start_date=None, end_date=None):

        return MarketDaily(code, start_date, end_date)
