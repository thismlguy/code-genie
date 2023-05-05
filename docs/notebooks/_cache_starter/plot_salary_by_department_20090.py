import matplotlib.pyplot as plt

def plot_salary_by_department(df):
    df.boxplot(column='salary', by='department')
    plt.title('Salary by Department')
    plt.xlabel('Department')
    plt.ylabel('Salary')
    plt.show()
