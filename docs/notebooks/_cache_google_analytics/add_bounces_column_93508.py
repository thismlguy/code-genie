import pandas as pd

def add_bounces_column(df):
    df['bounces'] = df['totals'].apply(lambda x: True if 'bounces' in x and x['bounces'] == 1 else False)
    return df
