
def run(df):
    df["action_type"] = df["hits"].apply(lambda x: int(x["eCommerceAction"]["action_type"]))
    return df
