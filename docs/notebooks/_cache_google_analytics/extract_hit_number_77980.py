import pandas as pd

def extract_hit_number(df):
    df['hit_number'] = df['hits'].apply(lambda x: x.get('hitNumber'))
    return df
