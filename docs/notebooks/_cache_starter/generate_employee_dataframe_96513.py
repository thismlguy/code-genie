import pandas as pd
import random

def generate_employee_dataframe():
    id_list = [i for i in range(101, 201)]
    name_list = ['John', 'Jack', 'Alice', 'Bob', 'Mary', 'Jane', 'Peter', 'David', 'Sarah', 'Emily']
    salary_list = [random.randint(50000, 100000) for i in range(100)]
    department_list = ['Engineering', 'Product'] * 50
    data = {
        'id': id_list,
        'name': name_list,
        'salary': salary_list,
        'department': department_list
    }
    df = pd.DataFrame(data)
    return df
