# -*- coding: utf-8 -*-
import pandas as pd
import requests
from bs4 import BeautifulSoup
url='http://finance.naver.com/sise/sise_market_sum.nhn'
url2='https://finance.naver.com/sise/sise_market_sum.nhn?&page=2'

cosdak_url='https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1'

req=requests.get(url)
html=req.text
soup=BeautifulSoup(html,'html.parser')
tables = soup.select('table')
content = tables[1]
print(content)