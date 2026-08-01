import pandas as pd

df = pd.read_csv("dataset/IPL.csv", low_memory=False)


def top_batsmen():

    return df.groupby("batter")["runs_batter"].sum().sort_values(
        ascending=False
    ).head(10)


def top_bowlers():

    return df.groupby("bowler")["bowler_wicket"].sum().sort_values(
        ascending=False
    ).head(10)