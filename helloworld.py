# -*- coding: utf-8 -*-

import pandas as pd

df = {'one' : [1, 2, 3],
   'two' : [1, 2, 3],
   'three' : [10,20,30]}

df = pd.DataFrame(df, index=['a', 'b', 'c'])
df['other']=pd.Series([22,32,42], index=['a', 'b', 'c'])
low = pd.DataFrame([[7,6,5,4]], columns=['one', 'two', 'three', 'other'])
print(df)
print('----')
print(len(df))
df = df.append(low)
print(len(df))

print('----')
k1 = df.iloc[0]
k2 = df.iloc[1]
k3=k1-k2
df.iloc[1]=k3
print(df)

