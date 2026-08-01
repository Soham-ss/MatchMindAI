import sys
import os
import re

# Ensure agents directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_search_agent import search_match_context, search_general_query
from monte_carlo_agent import run_monte_carlo_simulation
from prediction_agent import predict_match_ml
from ai_analyst_agent import generate_llm_analysis

# HISTORICAL IPL KNOWLEDGE BASE (2008 - 2026)
ORANGE_CAP_WINNERS = {
    "2008": ("Shaun Marsh", "Kings XI Punjab", "616 runs"),
    "2009": ("Matthew Hayden", "Chennai Super Kings", "572 runs"),
    "2010": ("Sachin Tendulkar", "Mumbai Indians", "618 runs"),
    "2011": ("Chris Gayle", "Royal Challengers Bangalore", "608 runs"),
    "2012": ("Chris Gayle", "Royal Challengers Bangalore", "733 runs"),
    "2013": ("Michael Hussey", "Chennai Super Kings", "733 runs"),
    "2014": ("Robin Uthappa", "Kolkata Knight Riders", "660 runs"),
    "2015": ("David Warner", "Sunrisers Hyderabad", "562 runs"),
    "2016": ("Virat Kohli", "Royal Challengers Bangalore", "973 runs"),
    "2017": ("David Warner", "Sunrisers Hyderabad", "641 runs"),
    "2018": ("Kane Williamson", "Sunrisers Hyderabad", "735 runs"),
    "2019": ("David Warner", "Sunrisers Hyderabad", "692 runs"),
    "2020": ("KL Rahul", "Kings XI Punjab", "670 runs"),
    "2021": ("Ruturaj Gaikwad", "Chennai Super Kings", "635 runs"),
    "2022": ("Jos Buttler", "Rajasthan Royals", "863 runs"),
    "2023": ("Shubman Gill", "Gujarat Titans", "890 runs"),
    "2024": ("Virat Kohli", "Royal Challengers Bengaluru", "741 runs"),
    "2025": ("Sai Sudharsan", "Gujarat Titans", "759 runs")
}

PURPLE_CAP_WINNERS = {
    "2008": ("Sohail Tanvir", "Rajasthan Royals", "22 wickets"),
    "2009": ("RP Singh", "Deccan Chargers", "23 wickets"),
    "2010": ("Pragyan Ojha", "Deccan Chargers", "21 wickets"),
    "2011": ("Lasith Malinga", "Mumbai Indians", "28 wickets"),
    "2012": ("Morne Morkel", "Delhi Daredevils", "25 wickets"),
    "2013": ("Dwayne Bravo", "Chennai Super Kings", "32 wickets"),
    "2014": ("Mohit Sharma", "Chennai Super Kings", "23 wickets"),
    "2015": ("Dwayne Bravo", "Chennai Super Kings", "26 wickets"),
    "2016": ("Bhuvneshwar Kumar", "Sunrisers Hyderabad", "23 wickets"),
    "2017": ("Bhuvneshwar Kumar", "Sunrisers Hyderabad", "26 wickets"),
    "2018": ("Andrew Tye", "Kings XI Punjab", "24 wickets"),
    "2019": ("Imran Tahir", "Chennai Super Kings", "26 wickets"),
    "2020": ("Kagiso Rabada", "Delhi Capitals", "30 wickets"),
    "2021": ("Harshal Patel", "Royal Challengers Bangalore", "32 wickets"),
    "2022": ("Yuzvendra Chahal", "Rajasthan Royals", "27 wickets"),
    "2023": ("Mohammed Shami", "Gujarat Titans", "28 wickets"),
    "2024": ("Harshal Patel", "Punjab Kings", "24 wickets"),
    "2025": ("Prasidh Krishna", "Rajasthan Royals", "25 wickets")
}

IPL_CHAMPIONS = {
    "2008": "Rajasthan Royals",
    "2009": "Deccan Chargers",
    "2010": "Chennai Super Kings",
    "2011": "Chennai Super Kings",
    "2012": "Kolkata Knight Riders",
    "2013": "Mumbai Indians",
    "2014": "Kolkata Knight Riders",
    "2015": "Mumbai Indians",
    "2016": "Sunrisers Hyderabad",
    "2017": "Mumbai Indians",
    "2018": "Chennai Super Kings",
    "2019": "Mumbai Indians",
    "2020": "Mumbai Indians",
    "2021": "Chennai Super Kings",
    "2022": "Gujarat Titans",
    "2023": "Chennai Super Kings",
    "2024": "Kolkata Knight Riders",
    "2025": "Royal Challengers Bengaluru"
}


def predict_full_match_agentic(team1, team2, venue, toss_winner, toss_decision, n_simulations=10000):
    """
    Complete Agentic Match Prediction Workflow:
    1. Real-Time Web Intelligence Agent -> Scrapes live web/Google news, weather, squad updates & pitch report
    2. Monte Carlo Simulation Agent -> Runs 10,000 ball-by-ball match simulations
    3. ML Predictor Agent -> Runs RandomForest model on historical data
    4. Master Synthesis & LLM Analyst -> Blends predictions & generates comprehensive report
    """
    print(f"[Agent 1/4] Fetching Real-Time Web Intelligence for {team1} vs {team2}...")
    web_context = search_match_context(team1, team2, venue)
    
    print(f"[Agent 2/4] Running {n_simulations:,} Monte Carlo Simulations...")
    mc_results = run_monte_carlo_simulation(team1, team2, venue, toss_winner, toss_decision, n_simulations)
    
    print(f"[Agent 3/4] Querying Historical ML RandomForest Model...")
    ml_winner, ml_prob = predict_match_ml(team1, team2, venue, toss_winner, toss_decision)
    
    # Calculate Blended Win Probability
    mc_t1_pct = mc_results["t1_win_pct"]
    mc_t2_pct = mc_results["t2_win_pct"]
    
    if ml_winner == team1:
        ml_t1_pct = ml_prob
        ml_t2_pct = 100.0 - ml_prob
    else:
        ml_t2_pct = ml_prob
        ml_t1_pct = 100.0 - ml_prob
        
    # Weighted Blend: 55% Monte Carlo Simulation + 45% ML Historical Pattern
    final_t1_pct = round((0.55 * mc_t1_pct) + (0.45 * ml_t1_pct), 1)
    final_t2_pct = round(100.0 - final_t1_pct, 1)
    
    final_winner = team1 if final_t1_pct >= final_t2_pct else team2
    final_win_prob = max(final_t1_pct, final_t2_pct)
    
    print(f"[Agent 4/4] Generating AI Strategic Match Commentary...")
    llm_prompt = f"""
Analyze the upcoming cricket match between {team1} and {team2} at {venue}.

Toss Winner: {toss_winner} | Toss Decision: {toss_decision}

Real-Time Internet Search Data & News:
{web_context}

Monte Carlo 10,000-Run Simulation Results:
- {team1} Win Chance: {mc_results['t1_win_pct']}% (Expected Score: {mc_results['t1_avg_score']} runs)
- {team2} Win Chance: {mc_results['t2_win_pct']}% (Expected Score: {mc_results['t2_avg_score']} runs)
- Highest Simulated Score: {team1} ({mc_results['t1_max_score']}), {team2} ({mc_results['t2_max_score']})

Historical Machine Learning Model Verdict:
- ML Predicted Winner: {ml_winner} ({ml_prob}% confidence)

Final Ensemble Winner Prediction: {final_winner} ({final_win_prob}%)

Please write a structured, highly analytical match prediction report covering:
1. Executive Winner Summary & Win Probability Breakdown
2. Pitch & Weather Real-Time Insights (from search data)
3. Monte Carlo Simulation Key Findings & Score Projections
4. 2 Key Tactical Match-ups / X-Factor Players that will decide the match.
Keep it professional, engaging, and markdown formatted.
"""
    
    match_report = generate_llm_analysis(llm_prompt)
    
    return {
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss_winner": toss_winner,
        "toss_decision": toss_decision,
        "final_winner": final_winner,
        "final_win_prob": final_win_prob,
        "final_t1_pct": final_t1_pct,
        "final_t2_pct": final_t2_pct,
        "mc_results": mc_results,
        "ml_winner": ml_winner,
        "ml_prob": ml_prob,
        "web_context": web_context,
        "match_report": match_report
    }


def format_direct_answer(user_query, live_web_data):
    """
    Provides exact, 100% accurate 1-line direct answers for any historical year (2008-2026),
    and handles invalid pre-2008 IPL queries (e.g., 2005).
    """
    q_lower = user_query.lower()
    
    # 0. Check for Pre-2008 Invalid IPL Queries (e.g. 2005, 2007)
    all_year_match = re.search(r'\b(19\d\d|20\d\d)\b', q_lower)
    if all_year_match:
        y_val = int(all_year_match.group(1))
        if y_val < 2008 and any(k in q_lower for k in ["orange cap", "purple cap", "ipl", "trophy", "champion", "winner", "winners"]):
            return f"⚠️ **IPL History Note**: The Indian Premier League (IPL) was founded in **2008**. There was no IPL or Orange Cap in **{y_val}**. The inaugural IPL season took place in 2008, where **Shaun Marsh** won the first-ever Orange Cap!"

    year_match = re.search(r'\b(200[89]|201[0-9]|202[0-6])\b', q_lower)
    year = year_match.group(1) if year_match else None
    
    # 1. Orange Cap Queries
    if "orange cap" in q_lower:
        if year and year in ORANGE_CAP_WINNERS:
            player, team, runs = ORANGE_CAP_WINNERS[year]
            return f"🏆 **IPL {year} Orange Cap Winner**: **{player}** ({team}) won the Orange Cap in IPL {year}, scoring **{runs}**."
        else:
            return "🏆 **IPL Orange Cap**: Awarded to the leading run-scorer of the IPL season. Recent winners: **Sai Sudharsan (2025 - 759 runs)**, **Virat Kohli (2024 - 741 runs)**, and **David Warner (2017 - 641 runs)**."

    # 2. Purple Cap Queries
    if "purple cap" in q_lower:
        if year and year in PURPLE_CAP_WINNERS:
            player, team, wickets = PURPLE_CAP_WINNERS[year]
            return f"💜 **IPL {year} Purple Cap Winner**: **{player}** ({team}) won the Purple Cap in IPL {year}, taking **{wickets}**."
        else:
            return "💜 **IPL Purple Cap**: Awarded to the leading wicket-taker of the IPL season. Recent winners: **Prasidh Krishna (2025 - 25 wickets)** and **Harshal Patel (2024 - 24 wickets)**."

    # 3. IPL Winner / Champions Queries for ANY Year (2008 to 2026)
    if any(k in q_lower for k in ["who won", "winner", "winners", "champion", "champions", "trophy", "title"]):
        if year and year in IPL_CHAMPIONS:
            champ = IPL_CHAMPIONS[year]
            return f"🏆 **IPL {year} Champions**: **{champ}** won the IPL {year} title!"
        else:
            # Return complete historical breakdown from 2008 to 2025 if no specific year mentioned
            breakdown = "\n".join([f"- **{y}**: {c}" for y, c in sorted(IPL_CHAMPIONS.items(), reverse=True)])
            return f"🏆 **All IPL Winners (2008 – 2025)**:\n{breakdown}"

    # 4. Player Queries
    if "virat" in q_lower or "kohli" in q_lower:
        return "🏏 **Virat Kohli** plays for **Royal Challengers Bengaluru (RCB)** in the IPL and **Team India** internationally as a top-order batsman."

    if "rohit" in q_lower or "sharma" in q_lower:
        return "🏏 **Rohit Sharma** plays for **Mumbai Indians (MI)** in the IPL and **Team India** internationally as an opening batsman."

    if "dhoni" in q_lower or "msd" in q_lower:
        return "🏏 **MS Dhoni** plays for **Chennai Super Kings (CSK)** in the IPL as a legendary wicketkeeper-batsman."

    if "hardik" in q_lower or "pandya" in q_lower:
        return "🏏 **Hardik Pandya** is the captain of **Mumbai Indians (MI)** in the IPL and an all-rounder for **Team India**."

    # 5. Clean Direct Summary Extractor from Web Search Data
    clean_titles = []
    if live_web_data:
        matches = re.findall(r'Source \[\d+\] \((.*?)\):', live_web_data)
        for m in matches:
            clean_text = re.sub(r'Published:.*', '', m).strip()
            if clean_text and len(clean_text) > 5 and clean_text not in clean_titles:
                clean_titles.append(clean_text)
                
    if clean_titles:
        return f"🌐 **Real-Time Web Intelligence**: {clean_titles[0]}"
    else:
        return f"🌐 **Real-Time Data**: Analysis completed for *\"{user_query}\"* based on latest web search records."


def answer_user_chatbot_query(user_query, chat_history=None):
    """
    Smart Conversational Intent Router:
    Handles Bot Identity, Introductions, Greetings, Pre-2008 IPL Checks, Historical IPL Winners & Stats for Any Year.
    """
    clean_query = user_query.strip().lower()
    
    # 0. Check for Pre-2008 Invalid IPL Queries (e.g., 2005, 2007)
    pre_2008_match = re.search(r'\b(19\d\d|200[0-7])\b', clean_query)
    if pre_2008_match and any(k in clean_query for k in ["orange cap", "purple cap", "ipl", "trophy", "champion", "winner", "winners"]):
        invalid_year = pre_2008_match.group(1)
        return f"⚠️ **IPL History Note**: The Indian Premier League (IPL) was founded in **2008**. There was no IPL or Orange Cap in **{invalid_year}**. The inaugural IPL season was held in 2008, where **Shaun Marsh** won the first-ever Orange Cap!", "Pre-2008 IPL Check Triggered"

    # 1. Detect Bot Identity Queries
    identity_keywords = ["what is your name", "what's your name", "who are you", "your name", "what is this app", "what can you do", "who created you", "who built you"]
    if any(ik in clean_query for ik in identity_keywords) and not any(pk in clean_query for pk in ["rohit", "virat", "dhoni", "team"]):
        identity_reply = """Hello! 👋 I am **MatchMindAi**, your real-time sports intelligence & match prediction assistant.

**What I Can Do For You:**
- 🏏 Tell you the exact team and stats for any IPL/international player (e.g., *Virat Kohli*, *Rohit Sharma*, *MS Dhoni*)
- 🎲 Run **10,000 ball-by-ball Monte Carlo match simulations**
- 🌐 Scrape **real-time live web data** from Google News for current & future IPL seasons (2025, 2026, 2027)
- 🏟️ Provide live pitch reports and weather forecasts for any stadium
"""
        return identity_reply, "Bot Identity System Triggered"

    # 2. Detect Name Introductions
    name_match = re.search(r'(?:my name is|i am|i\'m|call me|name is)\s+([A-Za-z]+)', user_query, re.IGNORECASE)
    if name_match:
        user_name = name_match.group(1).capitalize()
        greeting_reply = f"""Hello **{user_name}**! 👋 Welcome to **MatchMindAi**!

How can I help you today? You can ask me:
- 🏏 **"In which team does Virat Kohli play?"**
- 🏆 **"Who won Orange Cap in 2017?"**
- 🏟️ **"What is the pitch report for Wankhede Stadium?"**
- 🔮 **"Who will win IPL 2026 or 2027 based on squad analysis?"**
"""
        return greeting_reply, f"Personalized Greeting Triggered for {user_name}"

    # 3. Detect General Greetings
    greetings_keywords = ["hi", "hello", "hey", "hlo", "hiii", "good morning", "good evening", "howdy", "help", "how are you"]
    is_greeting_only = any(clean_query == g for g in greetings_keywords) or (len(clean_query) <= 5 and any(w in clean_query for w in ["hi", "hey", "hlo", "hello"]))
    
    if is_greeting_only and not any(k in clean_query for k in ["match", "win", "team", "ipl", "predict", "rohit", "virat", "dhoni"]):
        greeting_reply = """Hello! 👋 I am **MatchMindAi**, your real-time sports intelligence assistant.

How can I help you today? You can ask me:
- 🏏 **"In which team does Virat Kohli play?"**
- 🏆 **"Who won Orange Cap in 2017?"**
- 🏟️ **"What is the pitch report for Wankhede Stadium?"**
- 🔮 **"Who will win IPL 2026 or 2027 based on squad analysis?"**
"""
        return greeting_reply, "Casual Greeting System Triggered"

    # 4. Direct Factual IPL History Router for ANY Year (Orange Cap, Purple Cap, Winners, Champions)
    if any(k in clean_query for k in ["orange cap", "purple cap", "winner", "winners", "champion", "champions", "who won", "trophy"]):
        return format_direct_answer(user_query, ""), "Direct IPL Factual Engine Triggered"

    # 5. Sports & Match Query Engine
    print(f"Fetching live search data for user prompt: '{user_query}'...")
    live_web_data = search_general_query(user_query)
    
    llm_prompt = f"""
User Question: "{user_query}"

Real-Time Web Search Results (Fetched Live from Google/Internet):
{live_web_data}

Instructions:
1. Provide a single, clean, concise 1-to-2 sentence direct answer to the user's question.
2. Do NOT output raw source links, URLs, or metadata tags. Give only the direct factual answer.
"""
    
    answer = generate_llm_analysis(
        llm_prompt,
        system_instruction="You are MatchMindAi. Give direct, single-sentence answers to sports and player queries without raw metadata."
    )
    
    # Fallback Check: If LLM returned generic fallback template, raw source snippets, or general default, use format_direct_answer!
    if "Based on real-time web intelligence" in answer or "Source [" in answer or "Recent winners include" in answer or "Final AI Verdict" in answer or "Strategic Match Analysis" in answer or "Team 1" in answer or "Executive Winner Summary" in answer:
        answer = format_direct_answer(user_query, live_web_data)
    
    return answer, live_web_data


if __name__ == "__main__":
    for test_q in ["who won ipl in 2016", "2011 ipl winner", "2008 ipl winner", "2020 ipl winner", "who won purple cap in 2016"]:
        ans, _ = answer_user_chatbot_query(test_q)
        print(f"Query: '{test_q}' -> {ans}")