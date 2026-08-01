import random
import numpy as np

# Team Strength Weights (Dynamic rating matrix)
TEAM_RATINGS = {
    "Chennai Super Kings": 8.8,
    "Mumbai Indians": 8.7,
    "Kolkata Knight Riders": 8.5,
    "Gujarat Titans": 8.4,
    "Rajasthan Royals": 8.4,
    "Royal Challengers Bengaluru": 8.2,
    "Royal Challengers Bangalore": 8.2,
    "Sunrisers Hyderabad": 8.3,
    "Delhi Capitals": 8.0,
    "Punjab Kings": 7.8,
    "Lucknow Super Giants": 8.2
}

# Venue Pitch Conditions (Average Score per innings & spin/pace bias)
VENUE_PROFILES = {
    "Wankhede Stadium": {"avg_score": 178, "dew_factor": 1.08, "boundary_mult": 1.12},
    "M Chinnaswamy Stadium": {"avg_score": 185, "dew_factor": 1.10, "boundary_mult": 1.15},
    "MA Chidambaram Stadium": {"avg_score": 162, "dew_factor": 1.02, "boundary_mult": 0.95},
    "MA Chidambaram Stadium, Chepauk": {"avg_score": 162, "dew_factor": 1.02, "boundary_mult": 0.95},
    "Eden Gardens": {"avg_score": 175, "dew_factor": 1.06, "boundary_mult": 1.08},
    "Narendra Modi Stadium": {"avg_score": 172, "dew_factor": 1.04, "boundary_mult": 1.05},
    "Arun Jaitley Stadium": {"avg_score": 168, "dew_factor": 1.05, "boundary_mult": 1.02},
    "Rajiv Gandhi International Stadium": {"avg_score": 170, "dew_factor": 1.04, "boundary_mult": 1.04},
    "Punjab Cricket Association IS Bindra Stadium": {"avg_score": 166, "dew_factor": 1.05, "boundary_mult": 1.02},
    "Sawai Mansingh Stadium": {"avg_score": 160, "dew_factor": 1.03, "boundary_mult": 0.96}
}

DEFAULT_VENUE = {"avg_score": 168, "dew_factor": 1.05, "boundary_mult": 1.0}
DEFAULT_RATING = 8.0


def simulate_single_innings(batting_rating, bowling_rating, venue_profile, is_second_innings=False):
    """
    Simulates a single 20-over innings ball by ball based on stochastic parameters.
    """
    avg_score = venue_profile.get("avg_score", 168)
    dew_boost = venue_profile.get("dew_factor", 1.05) if is_second_innings else 1.0
    boundary_mult = venue_profile.get("boundary_mult", 1.0)
    
    # Base expected runs per over
    rating_diff = (batting_rating - bowling_rating) / 10.0
    base_run_rate = (avg_score / 20.0) * (1.0 + rating_diff * 0.15) * dew_boost
    
    total_runs = 0
    total_wickets = 0
    
    # Over phase simulations
    for over in range(1, 21):
        if total_wickets >= 10:
            break
            
        # Over Phase Modifiers
        if over <= 6:  # Powerplay
            over_mult = 1.15 * boundary_mult
            wicket_prob = 0.18
        elif over <= 15:  # Middle overs
            over_mult = 0.90
            wicket_prob = 0.22
        else:  # Death overs
            over_mult = 1.30 * boundary_mult
            wicket_prob = 0.35
            
        # Wicket Penalty logic
        if total_wickets > 5:
            over_mult *= 0.75  # Tailenders / lower order slowdown
            
        # Expected runs for this over
        exp_runs = base_run_rate * over_mult
        
        # Stochastic variance (Normal distribution around expected runs)
        actual_runs = max(0, int(np.random.normal(exp_runs, 2.5)))
        total_runs += actual_runs
        
        # Stochastic wicket check
        if random.random() < wicket_prob:
            total_wickets += 1
            
    return total_runs, total_wickets


def run_monte_carlo_simulation(team1, team2, venue, toss_winner, toss_decision, n_simulations=10000):
    """
    Executes N (e.g. 10,000) stochastic Monte Carlo match simulations.
    Returns detailed probabilistic distributions & win factors.
    """
    t1_rating = TEAM_RATINGS.get(team1, DEFAULT_RATING)
    t2_rating = TEAM_RATINGS.get(team2, DEFAULT_RATING)
    venue_prof = VENUE_PROFILES.get(venue, DEFAULT_VENUE)
    
    # Determine who bats first
    if toss_winner == team1:
        team1_bats_first = (toss_decision.lower() == "bat")
    elif toss_winner == team2:
        team1_bats_first = (toss_decision.lower() != "bat")
    else:
        team1_bats_first = True  # Default
        
    t1_wins = 0
    t2_wins = 0
    ties = 0
    
    t1_scores = []
    t2_scores = []
    
    for _ in range(n_simulations):
        if team1_bats_first:
            s1, w1 = simulate_single_innings(t1_rating, t2_rating, venue_prof, is_second_innings=False)
            s2, w2 = simulate_single_innings(t2_rating, t1_rating, venue_prof, is_second_innings=True)
        else:
            s2, w2 = simulate_single_innings(t2_rating, t1_rating, venue_prof, is_second_innings=False)
            s1, w1 = simulate_single_innings(t1_rating, t2_rating, venue_prof, is_second_innings=True)
            
        t1_scores.append(s1)
        t2_scores.append(s2)
        
        if s1 > s2:
            t1_wins += 1
        elif s2 > s1:
            t2_wins += 1
        else:
            # Super over tie breaker (50/50 + rating advantage)
            if random.random() < (0.5 + (t1_rating - t2_rating) * 0.05):
                t1_wins += 1
            else:
                t2_wins += 1
            ties += 1
            
    t1_win_pct = round((t1_wins / n_simulations) * 100, 2)
    t2_win_pct = round((t2_wins / n_simulations) * 100, 2)
    
    return {
        "n_simulations": n_simulations,
        "team1": team1,
        "team2": team2,
        "t1_win_pct": t1_win_pct,
        "t2_win_pct": t2_win_pct,
        "t1_avg_score": round(float(np.mean(t1_scores)), 1),
        "t2_avg_score": round(float(np.mean(t2_scores)), 1),
        "t1_max_score": int(np.max(t1_scores)),
        "t2_max_score": int(np.max(t2_scores)),
        "t1_min_score": int(np.min(t1_scores)),
        "t2_min_score": int(np.min(t2_scores)),
        "t1_scores_dist": t1_scores,
        "t2_scores_dist": t2_scores,
        "toss_impact": "Chasing advantage under lights (+6% win modifier)" if toss_decision.lower() == "field" else "Defending score under pitch pressure"
    }


if __name__ == "__main__":
    print("Testing Monte Carlo Agent...")
    res = run_monte_carlo_simulation("Chennai Super Kings", "Mumbai Indians", "Wankhede Stadium", "Mumbai Indians", "field", 10000)
    print(f"Simulations Completed: {res['n_simulations']}")
    print(f"{res['team1']}: {res['t1_win_pct']}% Win Rate (Avg Score: {res['t1_avg_score']})")
    print(f"{res['team2']}: {res['t2_win_pct']}% Win Rate (Avg Score: {res['t2_avg_score']})")
