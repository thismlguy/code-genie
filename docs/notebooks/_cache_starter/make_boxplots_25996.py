import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def make_boxplots(df):
    plt.figure(figsize=(8,5))
    sns.boxplot(x='department', y='salary', data=df)
    plt.title('Salary distribution by Department')
    plt.show()
