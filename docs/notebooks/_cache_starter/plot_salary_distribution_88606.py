import pandas as pd
import matplotlib.pyplot as plt

def plot_salary_distribution(df):
    df = df.dropna(subset=['salary'])
    salary_bins = range(0, int(df['salary'].max()) + 10000, 10000)
    plt.hist(df['salary'], bins=salary_bins, edgecolor='black', alpha=0.5)
    plt.title('Salary Distribution')
    plt.xlabel('Salary')
    plt.ylabel('Frequency')
    plt.show()
