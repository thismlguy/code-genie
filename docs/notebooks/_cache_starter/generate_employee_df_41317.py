import pandas as pd
import random

def generate_employee_df():
    employee_data = {"id": [random.randint(1000,9999) for i in range(100)],
                     "name": ["Employee_" + str(i) for i in range(1,101)],
                     "salary": [random.randint(40000,150000) for i in range(100)],
                     "department": ["engineering" if i<50 else "product" for i in range(100)]}
    
    employee_df = pd.DataFrame(employee_data)
    return employee_df
