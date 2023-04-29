import pandas as pd
import numpy as np

def count_high_earners(df):
    high_earners = df[df['salary'] > 100000].groupby('department')['id'].count()
    return high_earners
