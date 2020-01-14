# -*- coding: utf-8 -*-
import FinanceDataReader as fdr
import datetime
import pickle

import os

from env import DATA_PATH


def find_in_file(code, end_date):
    file_name = f'{DATA_PATH}/daily_history_{code}_{end_date}.pkl'
    if (os.path.isfile(file_name)):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    else:
        return None
    pass


def save_in_file(df, code, end_date):
    file_name = f'{DATA_PATH}/daily_history_{code}_{end_date}.pkl'
    with open(file_name, 'wb') as f:
        return pickle.dump(df, f)



def MarketDaily(code, start_date=None, end_date=None):
    if start_date is None:
        start_date = '1992-01-01'
    if end_date is None:
        today = datetime.date.today()
        end_date = today.strftime('%Y-%m-%d')

    df = find_in_file(code, end_date)
    if df is None:
        # Samsung(005930), 1992-01-01 ~ 2018-10-31
        df = fdr.DataReader(code, start_date, end_date)
        save_in_file(df, code, end_date)
    decorate(df)

    return df


def decorate(df):
    mas = [5, 20, 60, 120, 240, 360]

    mDict = {}
    for ma in mas:
        mDict[ma] = df['Close'].rolling(window=ma).mean()
        key = f'MA{ma}'
        if key not in df.columns:
            df.insert(len(df.columns), key, mDict[ma])

    df.insert(len(df.columns), 'GOLD_CROSS', df['MA5'] > df['MA20'])
    df['GOLD_CROSS'] = df['GOLD_CROSS'].apply(lambda x: 1 if x is True else 0)
