import seaborn as sns

def plot_salary_distribution(df):
    sns.set(style="whitegrid")
    sns.displot(data=df, x="salary", hue="work_year", kind="kde", fill=True)
