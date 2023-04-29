import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math

def plot_salary_distribution(df):
    bins = range(math.floor(df.salary.min()/10000)*10000, math.ceil(df.salary.max()/10000)*10000, 10000)
    plt.hist(df.salary, bins=bins)
    plt.xticks(bins)
    plt.xlabel('Salary')
    plt.ylabel('Number of Employees')
    plt.title('Distribution of Salary')
    plt.show()
