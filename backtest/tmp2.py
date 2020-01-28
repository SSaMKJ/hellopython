# -*- coding: utf-8 -*-
from backtest.back_test import BackTest

import backtrader as bt

from backtest.starategies.TestStrategy import *

# high : 078070
# low : 036420

# [
#     {'code': '036420', 'rate': 0.52072},
#     {'code': '144960', 'rate': 0.97666},
#     {'code': '025320', 'rate': 1.14965},
#     {'code': '214370', 'rate': 1.896},
#     {'code': '088350', 'rate': 58.988}
# ]
# [{'code': '950180', 'rate': 59.2445},
#  {'code': '010060', 'rate': 59.859},
# {'code': '307950', 'rate': 60.197},
# {'code': '950110', 'rate': 61.6682},
#  {'code': '067080', 'rate': 62.641},
# {'code': '010170', 'rate': 63.2851},
# {'code': '036460', 'rate': 64.4185},
# {'code': '008930', 'rate': 64.79053},
# {'code': '068270', 'rate': 66.72305},
# {'code': '066970', 'rate': 67.1075},
#  {'code': '028300', 'rate': 68.913},
# {'code': '009970', 'rate': 70.155},
# {'code': '006840', 'rate': 70.848},
# {'code': '008350', 'rate': 70.97125},
# {'code': '042660', 'rate': 70.975},
# {'code': '226320', 'rate': 71.1275},
# {'code': '078600', 'rate': 72.2245},
# {'code': '097950', 'rate': 72.27},
# {'code': '081660', 'rate': 72.4925},
# {'code': '251970', 'rate': 72.545}]



# [
#     {'code': '111710', 'rate': 211.1834},
#     {'code': '084850', 'rate': 214.494},
#     {'code': '035720', 'rate': 234.432},
#     {'code': '179900', 'rate': 274.193},
#     {'code': '078070', 'rate': 390.1665}
# ]
# https://finance.naver.com/item/main.nhn?code=036540
code = '052690'
back_test = BackTest(code, date_str='2020-01-18', isLogging=False)
back_test.set_strategy(TestStrategy_2)
rate = back_test.run() * 100 / 10000000

back_test.plot()

'''
판매전략1. 오늘 거래량이 최근 최대였다면 다음날 판다.
참고: 111710

'''