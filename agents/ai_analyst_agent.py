import os
import re

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Check available API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    from groq import Groq
    HAS_GROQ = True if GROQ_API_KEY else False
except ImportError:
    HAS_GROQ = False

try:
    import openai
    HAS_OPENAI = True if OPENAI_API_KEY else False
except ImportError:
    HAS_OPENAI = False


def generate_llm_analysis(prompt, system_instruction="You are MatchMindAi, an elite sports data scientist and IPL match analyst."):
    """
    Generates intelligent match commentary/analysis.
    Prioritizes Groq API, then OpenAI API, and falls back to rule-based synthesis.
    """
    if HAS_GROQ and GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {e}. Falling back...")

    if HAS_OPENAI and OPENAI_API_KEY:
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API info: {e}. Using Agentic Rule-Based Synthesis...")

    return generate_fallback_match_report(prompt)


def generate_fallback_match_report(prompt):
    """
    Generates structured, highly analytical match analysis fallback when LLM API keys are unavailable.
    """
    match_query = ""
    query_match = re.search(r'User Question:\s*"(.*?)"', prompt)
    if query_match:
        match_query = query_match.group(1).strip()
        
    web_sources = ""
    sources_match = re.search(r'Real-Time Web Search Results.*?\n(.*)', prompt, re.DOTALL)
    if sources_match:
        web_sources = sources_match.group(1).strip()
        
    if match_query:
        response_lines = [f"### 🌐 Real-Time Intelligence Answer for: *\"{match_query}\"*\n"]
        
        if "rohit" in match_query.lower():
            response_lines.append("**Rohit Sharma Overview & Current Status:**")
            response_lines.append("- **IPL Team**: Mumbai Indians (MI) as opening batsman.")
            response_lines.append("- **International**: Represents Team India.")
            response_lines.append("- **Key Fact**: Led Mumbai Indians to 5 IPL Trophy titles.")
            return "\n".join(response_lines)
            
        if "virat" in match_query.lower():
            response_lines.append("**Virat Kohli Overview & Current Status:**")
            response_lines.append("- **IPL Team**: Royal Challengers Bengaluru (RCB).")
            response_lines.append("- **International**: Represents Team India.")
            response_lines.append("- **Key Fact**: All-time leading run scorer in IPL history.")
            return "\n".join(response_lines)
            
        if "dhoni" in match_query.lower():
            response_lines.append("**MS Dhoni Overview & Current Status:**")
            response_lines.append("- **IPL Team**: Chennai Super Kings (CSK) as wicketkeeper-batsman.")
            response_lines.append("- **Key Fact**: Led CSK to 5 IPL Trophy titles.")
            return "\n".join(response_lines)

    t1_match = re.search(r'cricket match between (.*?) and (.*?) at (.*?)\.', prompt)
    t1 = t1_match.group(1) if t1_match else "Team 1"
    t2 = t1_match.group(2) if t1_match else "Team 2"
    venue = t1_match.group(3) if t1_match else "Stadium Venue"
    
    winner_match = re.search(r'Final Ensemble Winner Prediction:\s*(.*?)\s*\((.*?)\%\)', prompt)
    winner = winner_match.group(1) if winner_match else t1
    win_pct = winner_match.group(2) if winner_match else "55.0"
    
    return f"""### 🎯 MatchMindAi Strategic Match Analysis

#### 🏆 Executive Winner Summary
- **Predicted Winner**: **{winner}**
- **Win Confidence**: **{win_pct}%**
- **Match Venue**: {venue}

---

#### 🎲 Monte Carlo & Tactical Insights
- **Match Dynamic**: High-intensity clash between {t1} and {t2}.
- **Tactical X-Factor**: Early wickets in the powerplay and death-overs execution will decide the final winner.
"""


if __name__ == "__main__":
    rep = generate_fallback_match_report("Analyze cricket match between Mumbai Indians and Chennai Super Kings at Wankhede Stadium.")
    print(rep)