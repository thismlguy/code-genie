import seaborn as sns
import numpy as np
import datetime
import pandas as pd
import math
import matplotlib.pyplot as plt

def plot_salary_distribution(df):
    bins_array = np.arange(min(df['salary']), max(df['salary']) + 10000, 10000)
    plt.figure(figsize=(10,5))
    sns.histplot(df['salary'], bins=bins_array, edgecolor='black', linewidth=1)
    plt.xlabel("Salary")
    plt.ylabel("Frequency")
    plt.title("Salary Distribution")
    plt.show()
