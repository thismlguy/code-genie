import pandas as pd
import random

def generate_employee_dataframe():
    employee_data = {'id': range(1, 101),
                     'name': ['Employee_' + str(i) for i in range(1, 101)],
                     'salary': [random.randint(40000, 125000) for i in range(1, 101)],
                     'department': ['engineering' if i%2==0 else 'product' for i in range(1, 101)]}
    
    df = pd.DataFrame(employee_data)
    df.loc[df.sample(frac=0.1).index, 'salary'] = None
    
    return df
