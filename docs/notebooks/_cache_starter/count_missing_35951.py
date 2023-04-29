import pandas as pd
import numpy as np

def count_missing(df):
    return df.isna().sum()
