import pandas as pd


def calculate_mean(df: pd.DataFrame, multiplier: int) -> pd.DataFrame:
    mean_df = df.groupby("y").mean()
    return mean_df.mul(multiplier)
