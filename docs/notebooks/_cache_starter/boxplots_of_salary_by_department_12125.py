import seaborn as sns
import numpy as np
import datetime
import pandas as pd
import math
import matplotlib.pyplot as plt

def boxplots_of_salary_by_department(df):
    sns.boxplot(x='department', y='salary', data=df)
    plt.show()
