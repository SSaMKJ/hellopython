# -*- coding: utf-8 -*-

'''
오늘 날짜 또는 특정 날짜의 시가총액으로 정렬된 회사코드를 리턴한다.
'''
import datetime
import json
import os

from crawler.current_price import crawling_market_cap
from env import DATA_PATH


class MarketCap:

    def __init__(self):
        pass

    def load(self, limit=200, market='COSPI'):

        date_str = self.today_str()

        ret_data = self.find_in_file(date_str, market)
        if ret_data is None or len(ret_data) < limit:
            ret_data = crawling_market_cap(market)
            self.save_in_file(ret_data, date_str, market)
        return ret_data[:limit]

    @classmethod
    def save_in_file(cls, ret_data, date_str, market):
        file_name = f'{DATA_PATH}/market_cap_{market}_{date_str}.json'
        with open(file_name, 'w', encoding="utf-8") as f:
            f.writelines(json.dumps(ret_data, ensure_ascii=False))



    @classmethod
    def find_in_file(cls, date_str, market):
        file_name = f'{DATA_PATH}/market_cap_{market}_{date_str}.json'
        if(os.path.isfile(file_name)):
            with open(file_name, 'r', encoding="utf-8") as f:
                return json.loads(f.read())
        else:
            return None



    @classmethod
    def today_str(cls):
        today = datetime.date.today()
        return today.strftime('%Y-%m-%d')


# k = MarketCap().load(market='COSDAK')
# print(k)