import pandas as pd

df = pd.read_csv('ratings.csv',index_col='userId')
print(df['userId'])
