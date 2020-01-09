# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def crawling_market_cap(market):
    if market is "COSPI" :
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?&page='
    else :
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page='

    retVal = []
    for index in range(1, 21):
        trs = get_content__(url+str(index))
        for tr in trs:
            if len(tr.select('td')) > 10:
                retVal.append({
                    'code': extractCode__(tr)
                    , 'name': extractName__(tr)
                    , 'current': extractAt__(tr, 2)
                    , 'market_cap': extractAt__(tr, 6)
                    , 'foreigner_rate': extractAt__(tr, 8)
                    , 'volume': extractAt__(tr, 9)
                    , 'PER': extractAt__(tr, 10)
                    , 'ROE': extractAt__(tr, 11)
                })
    return retVal


def get_content__(url):
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.select('table')
    content = tables[1]
    return content.select('tr')


def extractCode__(tr):
    tds = tr.select('td')
    for td in tds:
        if ('code' in str(td)):
            str_tmp = str(td).split('code')[1]
            return str_tmp.split('"')[0][1:]


def extractName__(tr):
    tds = tr.select('td')
    for td in tds:
        if ('tltle' in str(td)):
            str_tmp = str(td).split('code')[1]
            return str_tmp.split('>')[1].split('<')[0]


def extractAt__(tr, index):
    tds = tr.select('td')
    return tds[index].text.replace(",","")
