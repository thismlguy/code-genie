def count_missing_values(df):
    """
    Function to count the number of missing values in each column of a pandas dataframe
    
    Parameters:
    df: pandas dataframe
    
    Returns: 
    missing_counts: pandas series with index as column names and values as count of missing values in each column
    """
    missing_counts = df.isnull().sum()
    return missing_counts