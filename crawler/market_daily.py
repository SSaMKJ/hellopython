import FinanceDataReader as fdr

# Samsung(005930), 1992-01-01 ~ 2018-10-31
df = fdr.DataReader('068270', '2020-01-01', '2020-01-07')
print(df)