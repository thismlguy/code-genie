import pandas as pd

def remote_ratio_mapper(df):
    df['remote_ratio'].replace({0: 'No Remote Work', 50: 'Partially Remote', 100: 'Fully Remote'}, inplace=True)
    return df
