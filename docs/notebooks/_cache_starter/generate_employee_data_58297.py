import pandas as pd
import random

def generate_employee_data():
    employee_ids = []
    employee_names = []
    salaries = []
    departments = []

    departments_list = ['engineering', 'product']
    
    for i in range(100):
        employee_ids.append(random.randint(100, 999))
        employee_names.append('Employee_' + str(i))
        salaries.append(random.randint(50000, 150000))
        departments.append(random.choice(departments_list))

    df = pd.DataFrame({
        'id': employee_ids,
        'name': employee_names,
        'salary': salaries,
        'department': departments
    })
    
    return df
