import pandas as pd

df = pd.read_csv("dataset/IPL.csv", low_memory=False)


def get_all_teams():
    return sorted(df["batting_team"].unique())


def get_team_runs(team_name):
    return df[df["batting_team"] == team_name]["runs_total"].sum()


def compare_teams(team1, team2):

    team1_runs = get_team_runs(team1)
    team2_runs = get_team_runs(team2)

    print("\n========== TEAM AGENT ANALYSIS ==========\n")

    print(f"{team1}")
    print(f"Total Runs : {team1_runs}\n")

    print(f"{team2}")
    print(f"Total Runs : {team2_runs}\n")

    print("--------------- RESULT ----------------")

    if team1_runs > team2_runs:
        print(f"{team1} has better batting statistics.")

    elif team2_runs > team1_runs:
        print(f"{team2} has better batting statistics.")

    else:
        print("Both teams are equally matched.")

    print("\n=========================================\n")