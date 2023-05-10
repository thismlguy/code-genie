import pandas as pd


def create_means_df(df):
    means_df = df.groupby("y").mean()
    return means_df
