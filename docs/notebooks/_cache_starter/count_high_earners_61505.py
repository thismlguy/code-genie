import pandas as pd

def count_high_earners(df):
    high_earners = df[df['salary'] > 100000].groupby('department').count()[['id']]
    high_earners.columns = ['count']
    return high_earners
