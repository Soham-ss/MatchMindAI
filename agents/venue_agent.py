import pandas as pd

df = pd.read_csv("dataset/IPL.csv", low_memory=False)


def top_venues():

    return df["venue"].value_counts().head(10)


def highest_scoring_venues():

    return df.groupby("venue")["runs_total"].mean().sort_values(
        ascending=False
    ).head(10)