# -*- coding: utf-8 -*-
import os
import json

import time

from crawler.market_daily import MarketDaily
from es.es_api import ES_API
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


# for i in range(min(20,len(df))):
#     key=df.index[i]
#     dt=int(time.mktime(key.timetuple()))
#     # print(hashlib.sha224(to__byte(key,'181710')).hexdigest())
#     ll=df.iloc[i].to_json()
#     j = json.loads(ll)
#     j['code']=code
#     j['date']=key
#     print(f'{code}-{dt}')
#     print(j)
#
# print(df.tail(2).index[0])
# print(df.tail(2).to_json(orient='records'))


'''
cospi top 400
cosdak top 500

data 가지고 오고 
데일리 데이터 가지고 와서
함 넣어 보자.

'''
code='181710'
ES_API('hello_today').dataInsert(code, 'COSPI', 'NHN', df)