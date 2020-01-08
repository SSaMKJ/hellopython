import FinanceDataReader as fdr
import datetime

today = datetime.date.today()

def MarketDaily(code, start_date=None, end_date=None):
    if start_date is None:
        start_date = '1992-01-01'
    if end_date is None:
        today = datetime.date.today()
        end_date = today.strftime('%Y-%m-%d')

    # Samsung(005930), 1992-01-01 ~ 2018-10-31
    df = fdr.DataReader(code, start_date, end_date)
    print(df)
    return df
