
def run(df):
    df["hit_type"] = df["hits"].apply(lambda x: x["type"])
    return df
