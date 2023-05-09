import matplotlib.pyplot as plt
import pandas as pd

def remote_ratio_by_work_years(df):
    """
    This function creates a bar chart of percentage counts of remote_ratio grouped by work_years.

    Parameters:
    df (pd.DataFrame): pandas dataframe with columns 'work_year', 'experience_level', 'employment_type',
                        'job_title', 'salary', 'employee_residence', 'remote_ratio', 'company_location', 
                        'company_size'.
                        
    Returns:
    None (displays a bar chart)
    """
    # Group by work year and remote ratio to get counts
    counts = df.groupby(['work_year', 'remote_ratio']).size().reset_index(name='count')
    
    # Group by work year to get total count for each year
    total_counts = counts.groupby('work_year').agg({'count': 'sum'}).reset_index()
    total_counts.rename(columns={'count': 'total_count'}, inplace=True)
    
    # Merge counts with total counts
    counts = counts.merge(total_counts, on=['work_year'])
    
    # Calculate percentage counts
    counts['percentage_count'] = counts['count'] / counts['total_count'] * 100
    
    # Pivot the table to create bar chart
    counts_pivot = counts.pivot(index='work_year', columns='remote_ratio', values='percentage_count')
    
    # Create the bar chart
    ax = counts_pivot.plot(kind='bar', stacked=True, figsize=(10, 6))
    ax.set_xlabel('Work Years')
    ax.set_ylabel('Percentage Count')
    ax.set_title('Remote Ratio by Work Years')
    plt.show()
