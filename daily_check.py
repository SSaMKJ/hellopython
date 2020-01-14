# -*- coding: utf-8 -*-

'''
crawling today market cap. cospi, cosdak
'''
import datetime
import json

import sys

from env import CONF_PATH
from service.daily_data import DailyData
from service.market_cap import MarketCap
from service.send_email import Send_EMail

marketCap = MarketCap()

cospi = marketCap.load(limit=100 * 2, market='COSPI')

daily = DailyData()


def month_ago(month):
    dt_date = datetime.date.today() - datetime.timedelta(days=month * 30)

    return dt_date.strftime('%Y-%m-%d')


for cos in cospi:
    # print(cos)
    try:
        roe = float(cos['ROE'])
    except Exception:
        continue

    if roe < 0:
        continue
    cosDF = daily.get_daily(cos['code'])
    month = month_ago(6)
    recent = cosDF.query('index>=%r' % month)
    # print(recent)
    maxHigh = recent['High'].max()
    if float(cos['current']) < (1.0 - 0.3) * maxHigh:
        print(cos)
        print('found!!!')


def gethering_codes():
    limits = [300, 200]
    markets = ['COSPI', 'COSDAK']

    marketCap = MarketCap()
    daily = DailyData()
    stocks = []
    for i in range(len(markets)):
        stocks_info = marketCap.load(limit=limits[i], market=markets[i])

        for cos in stocks_info:
            # print(cos)
            try:
                roe = float(cos['ROE'])
            except Exception:
                continue

            if roe < 0:
                continue
            cosDF = daily.get_daily(cos['code'])
            month = month_ago(6)
            recent = cosDF.query('index>=%r' % month)
            # print(recent)
            maxHigh = recent['High'].max()
            if float(cos['current']) < (1.0 - 0.3) * maxHigh:
                print(cos)
                print('found!!!')
                stocks.append({'code': cos['code'], 'name': cos['name'], 'market': markets[i],
                               'ratio': 1-(float(cos['current']) / maxHigh)})
    return stocks


def filter_ignores(codes):
    with open(f'{CONF_PATH}/ignore_codes.json') as f :
        ignores = json.load(f)

    print(type(ignores))
    print(ignores)

    ret_codes = []
    for c in codes:
        if c['code'] not in ignores:
            ret_codes.append(c)

    return ret_codes


def send_emails(codes):
    html = []
    html.append("""<html><meta charset="utf-8">
        <head></head>
        <body>""")

    for stock in codes:
        html.append(get_ul(stock))

    html.append("""
    </body></html>
    """)

    Send_EMail().send_email("ssamkj@gmail.com", "오늘 ", "".join(html))
    print(codes)


def get_ul(stock):
    ul = []
    ul.append("<ul>")
    ul.append("<li>")
    ul.append(f'<a href=https://finance.naver.com/item/main.nhn?code={stock["code"]} target="_blank">')
    ul.append(stock['name'])
    ul.append("</a>")
    ul.append("</li>")
    ul.append("<li>")
    ul.append(f'떨어진 비율 {stock["ratio"]}%')
    ul.append("</li>")
    ul.append("</ul>")
    print(ul)
    return "".join(ul)


def main():
    codes = gethering_codes()
    codes = filter_ignores(codes)
    codes = sorted(codes, key=lambda k: k['ratio'], reverse=True)
    send_emails(codes)


main()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('')
