import pandas as pd

def get_page_bounce_rate(df):
    hit1_page_df = df[(df["hit_number"] == 1) & (df["hit_type"] == "PAGE")]
    page_agg_df = hit1_page_df.groupby("page_path").agg(
        views=pd.NamedAgg(column="page_path", aggfunc="count"),
        bounce_rate=pd.NamedAgg(column="bounces", aggfunc=lambda x: sum(x)/len(x))
    ).sort_values("views", ascending=False)
    return page_agg_df
