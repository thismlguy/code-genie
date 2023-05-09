import pandas as pd

def map_experience_level(df):
    mapping = {'EN': 'Entry-level / Junior', 'MI': 'Mid-level / Intermediate', 
               'SE': 'Senior-level / Expert', 'EX': 'Executive-level / Director'}
    df['experience_level'] = df['experience_level'].map(mapping)
    return df