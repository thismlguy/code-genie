import pandas as pd

def extract_action_type(df):
    hits_list = []
    
    for row in df.itertuples(index=False):
        hits_dict = row.hits
        if 'eCommerceAction' in hits_dict.keys():
            ecommerce_dict = hits_dict['eCommerceAction']
            if 'action_type' in ecommerce_dict.keys():
                hits_dict.update({'action_type': ecommerce_dict['action_type']})
            else:
                hits_dict.update({'action_type': None})
        else:
            hits_dict.update({'action_type': None})
        hits_list.append(hits_dict)
    
    hits_df = pd.DataFrame(hits_list)

    df = pd.concat([df, hits_df['action_type']], axis=1)
    return df
