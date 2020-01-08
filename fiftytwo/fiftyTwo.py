# -*- coding: utf-8 -*-
import requests


def FiftyTwoWeekRange(stock_code):
    URL = f'https://finance.yahoo.com/quote/{stock_code}.KS?p={stock_code}.KS&.tsrc=fin-srch'
    response = requests.get(URL)
    return _extract_52_high_low(response.text)


def _extract_52_high_low(txt):
    key='fiftyTwoWeekRange'
    first_index =txt.index(key)
    print(first_index)
    raw1 = txt[first_index+len(key)+2:first_index+len(key)+100]
    raw_arr1 = raw1.split(",")
    high_low = raw_arr1[0].split(":")[1].replace('"','').replace(' ','').split("-")
    print(high_low)
    low = int(high_low[0].split(".")[0])
    high =  int(high_low[1].split(".")[0])
    print(low)
    print(high)
    return high, low
