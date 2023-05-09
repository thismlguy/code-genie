import matplotlib.pyplot as plt

def create_boxplot(df):
    plt.boxplot(df['salary'])
    plt.show()
