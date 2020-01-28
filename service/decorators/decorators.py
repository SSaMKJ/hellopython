# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


def add_mas(df, mas=[5, 20, 60, 120, 240, 360]):
    mas = [5, 20, 60, 120, 240, 360]

    mDict = {}
    for ma in mas:
        mDict[ma] = df['Close'].rolling(window=ma).mean()
        key = f'MA{ma}'
        if key not in df.columns:
            df.insert(len(df.columns), key, mDict[ma])

    df.insert(len(df.columns), 'GOLD_CROSS', df['MA5'] > df['MA20'])
    df['GOLD_CROSS'] = df['GOLD_CROSS'].apply(lambda x: 1 if x is True else 0)


def add_RSI(df, period=14, signal_mean=9):
    df.insert(len(df.columns), "RSI", calcRSI__(df, period))  # web.DataReader를 통해 받았던 원래 DataFrame에 'RSI'열을 추가
    df.insert(len(df.columns), "RSI signal",
              df['RSI'].rolling(window=signal_mean).mean())  # RSI signal(RSI 이동평균)을 구해서 추가함


def calcRSI__(df, period):
    date_index = df.index.astype('str')

    U = np.where(df.diff(1)['Close'] > 0, df.diff(1)['Close'],
                 0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 크면 증가분을 감소했으면 0을 넣어줌
    D = np.where(df.diff(1)['Close'] < 0, df.diff(1)['Close'] * (-1),
                 0)  # df.diff를 통해 (기준일 종가 - 기준일 전일 종가)를 계산하여 0보다 작으면 감소분을 증가했으면 0을 넣어줌
    AU = pd.DataFrame(U, index=date_index).rolling(window=period).mean()  # AU, period=14일 동안의 U의 평균
    AD = pd.DataFrame(D, index=date_index).rolling(window=period).mean()  # AD, period=14일 동안의 D의 평균
    RSI = AU / (AD + AU) * 100  # 0부터 1로 표현되는 RSI에 100을 곱함
    return RSI


def add_bollinger_band(df, period=20):
    ma20 = df['Close'].rolling(window=period).mean()  # 20일 이동평균값
    bol_upper = ma20 + 2 * df['Close'].rolling(window=period).std()  # BB(볼린저밴드) 상단 밴드
    bol_down = ma20 - 2 * df['Close'].rolling(window=period).std()  # BB(볼린저밴드) 하단 밴드 # 차트 레이아웃을 설정
    df.insert(len(df.columns), "bol_upper", bol_upper)
    df.insert(len(df.columns), "bol_down", bol_down)


def calMACD(df, short=12, long=26, signal=9):
    df['MACD'] = df['Close'].ewm(span=short, min_periods=long - 1, adjust=False).mean() - df['Close'].ewm(span=long,
                                                                                                         min_periods=long - 1,
                                                                                                         adjust=False).mean()
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, min_periods=signal - 1, adjust=False).mean()
    df.insert(len(df.columns), 'MACD_OSC', df['MACD'] - df['MACD_Signal'])


# 일자(n,m,t)에 따른 Stochastic(KDJ)의 값을 구하기 위해 함수형태로 만듬
def get_stochastic(df, n=15, m=5, t=3):
    # n일중 최고가
    ndays_high = df['High'].rolling(window=n, min_periods=1).max()
    # n일중 최저가
    ndays_low = df['Low'].rolling(window=n, min_periods=1).min()

    # Fast%K 계산

    df.insert(len(df.columns), 'Sto_K', ((df['Close'] - ndays_low) / (ndays_high - ndays_low)) * 100)
    # Fast%D (=Slow%K) 계산
    df.insert(len(df.columns), 'Sto_D', df['Sto_K'].ewm(span=m).mean())
    # Slow%D 계산
    df.insert(len(df.columns), 'Sto_SlowD', df['Sto_D'].ewm(span=t).mean())

from scipy.stats import linregress

def add_momentum(df):
    df.insert(len(df.columns), 'momentum', df['Close'].rolling(90).apply(momentum, raw=False))


def momentum(closes):
    returns = np.log(closes)
    x = np.arange(len(returns))
    slope, _, rvalue, _, _ = linregress(x, returns)
    # annualize slope and multiply by R^2
    return ((1 + slope) ** 252) * (rvalue ** 2)

