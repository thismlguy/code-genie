import numpy as np
import pandas as pd

def make_salaries_missing(df):
    np.random.seed(42)  # for reproducibility
    
    # get 10% of the employees and make their salaries missing
    n = int(len(df)*0.1)
    idx = np.random.choice(len(df), n, replace=False)
    df.loc[idx, 'salary'] = np.nan
    
    return df
