import seaborn as sns
import numpy as np

def plot_salary_distribution(df):
    bins = np.arange(0, df['salary'].max()+10000, 10000)
    sns.histplot(data=df, x='salary', kde=True, bins=bins)
