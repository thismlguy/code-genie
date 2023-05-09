import matplotlib.pyplot as plt

def top_jobs(df):
    top_jobs = df['job_title'].value_counts()[:15] # Get top 15 most frequently occurring job designations
    plt.bar(top_jobs.index, top_jobs.values) # Make bar chart
    plt.xticks(rotation=90) # Rotate labels
    for i, v in enumerate(top_jobs.values):
        plt.text(i, v+5, str(v), ha='center') # Print count on top of each bar
    plt.show() 
