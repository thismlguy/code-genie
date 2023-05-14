import pandas as pd

def aggregate_data(df):
    df_filtered = df[df['hit_type']=='PAGE']
    df_grouped = df_filtered.groupby('page_path').agg({'hit_type':'count','bounces':'mean'})
    df_grouped.columns = ['views','exit_rate']
    df_sorted = df_grouped.sort_values(by='views', ascending=False)
    return df_sorted
