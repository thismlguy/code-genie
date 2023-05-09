import matplotlib.pyplot as plt

def pie_chart(df):
    plt.pie(df['work_year'].value_counts(), labels=df['work_year'].unique())
    plt.title('Distribution of work year')
    plt.show()