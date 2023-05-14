import pandas as pd

def extract_page_path(df):
    # extract page path
    df['page_path'] = df['hits'].apply(lambda x: x['page']['pagePath'])
    
    return df
