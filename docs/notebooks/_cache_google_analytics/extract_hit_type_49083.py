import pandas as pd

def extract_hit_type(df):
    
    # Loop through the hits column and extract the hit type from the dictionary
    hit_types = []
    for row in df['hits']:
        hit_type = row['type']
        hit_types.append(hit_type)
    
    # Create a new column called hit_type with the extracted hit types
    df['hit_type'] = hit_types
    
    return df
