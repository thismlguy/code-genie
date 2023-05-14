import pandas as pd

def separate_hits(df):
    """
    Input:
    df: pandas dataframe with columns: Index(['visitorId', 'visitNumber', 'visitId', 'visitStartTime', 'date',
       'totals', 'trafficSource', 'device', 'geoNetwork', 'customDimensions',
       'hits', 'fullVisitorId', 'userId', 'clientId', 'channelGrouping',
       'socialEngagementType'],
      dtype='object')
    
    Output:
    new_df: pandas dataframe with separate rows for each item in the hits column and the same value for each item in the totals column
    """
    
    # create new dataframe with separate row for each item in hits column
    new_df = df.explode('hits')
    
    # drop columns except hits and totals
    new_df = new_df[['hits', 'totals']]
    
    return new_df
