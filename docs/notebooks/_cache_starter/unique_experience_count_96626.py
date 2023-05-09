import pandas as pd

def unique_experience_count(df):
    experience_counts = df['experience_level'].value_counts()
    print(experience_counts)
