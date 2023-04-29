import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import math

def make_salaries_missing(df):
    # get a sample of 10% of the employees to make salaries missing
    sample_size = int(df.shape[0] * 0.1)
    sample_ids = np.random.choice(df['id'], sample_size, replace=False)
    
    # set the salaries for the selected employees to be missing
    df.loc[df['id'].isin(sample_ids), 'salary'] = np.nan
    
    return df
