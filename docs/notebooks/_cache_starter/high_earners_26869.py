def high_earners(df):
    high_earners_df = df[df['salary'] > 100000]
    return high_earners_df.groupby('department').size()