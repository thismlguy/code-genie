import pandas as pd


def multiply_df(df: pd.DataFrame, multiplier: int) -> pd.DataFrame:
    df["x"] = df["x"] * multiplier
    return df
