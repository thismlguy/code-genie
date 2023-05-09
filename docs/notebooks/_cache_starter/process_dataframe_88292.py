import pandas as pd

def process_dataframe(df):
    df = df.drop(columns=['salary', 'salary_currency'])
    df = df.rename(columns={"salary_in_usd": "salary"})
    return df