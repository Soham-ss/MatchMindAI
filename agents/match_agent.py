
import pandas as pd

df = pd.read_csv("dataset/IPL.csv", low_memory=False)


def toss_statistics():

    return df["toss_winner"].value_counts().head(10)


def match_winners():

    return df["match_won_by"].value_counts().head(10)