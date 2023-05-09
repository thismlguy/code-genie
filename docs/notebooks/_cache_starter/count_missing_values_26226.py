import pandas as pd

def count_missing_values(df):
    return df.isnull().sum()
