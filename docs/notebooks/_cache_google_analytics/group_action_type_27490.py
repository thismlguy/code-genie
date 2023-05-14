import pandas as pd

def group_action_type(df):
    # group data by action_type and count number of rows in each group
    action_counts = df.groupby('action_type').size().reset_index(name='count')
    
    # remove action_type other than 1, 2, 5, 6
    action_counts = action_counts[action_counts['action_type'].isin([1, 2, 5, 6])]
    
    # replace the action_type values as:
    # 1: Click on product list page
    # 2: Product details page
    # 5: Checkout
    # 6: Purchase Complete
    action_counts['action_type'] = action_counts['action_type'].replace({1: 'Click on product list page', 2: 'Product details page', 5: 'Checkout', 6: 'Purchase Complete'})
    
    return action_counts
