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


    return df

