import matplotlib.pyplot as plt
import numpy as np

def plot_emp_type_experience_level(df):
    emp_types = df['employment_type'].unique()
    fig, axes = plt.subplots(1, len(emp_types), figsize=(15,5))
    for i, emp_type in enumerate(emp_types):
        data = df[df['employment_type'] == emp_type]['experience_level'].value_counts()
        axes[i].bar(data.index, data.values)
        axes[i].set_title(emp_type)
        axes[i].tick_params(axis='x', rotation=45)
    plt.show()
