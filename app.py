import os
import sys
import base64
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Ensure agents directory is in Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))

# Default Fallback Dictionaries
DEFAULT_TEAM_RATINGS = {
    "Chennai Super Kings": 88,
    "Mumbai Indians": 87,
    "Royal Challengers Bengaluru": 85,
    "Kolkata Knight Riders": 86,
    "Gujarat Titans": 84,
    "Rajasthan Royals": 85,
    "Sunrisers Hyderabad": 84,
    "Delhi Capitals": 82,
    "Punjab Kings": 81,
    "Lucknow Super Giants": 83
}

DEFAULT_VENUE_PROFILES = {
    "Wankhede Stadium": {"avg_score": 172, "dew_factor": 0.12},
    "M. Chinnaswamy Stadium": {"avg_score": 180, "dew_factor": 0.15},
    "MA Chidambaram Stadium": {"avg_score": 158, "dew_factor": 0.05},
    "Eden Gardens": {"avg_score": 168, "dew_factor": 0.10},
    "Narendra Modi Stadium": {"avg_score": 175, "dew_factor": 0.08}
}

try:
    from master_agent import predict_full_match_agentic, answer_user_chatbot_query
    from monte_carlo_agent import TEAM_RATINGS, VENUE_PROFILES
    from web_search_agent import search_realtime
except Exception as e:
    TEAM_RATINGS = DEFAULT_TEAM_RATINGS
    VENUE_PROFILES = DEFAULT_VENUE_PROFILES
    try:
        from web_search_agent import search_realtime
    except Exception:
        def search_realtime(q, max_results=5): return []

# Page Configuration
st.set_page_config(
    page_title="MatchMindAi - Real-Time Cricket Prediction & Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Convert Stadium Image to Base64
stadium_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stadium.jpg")
stadium_b64 = ""
if os.path.exists(stadium_img_path):
    with open(stadium_img_path, "rb") as img_file:
        stadium_b64 = base64.b64encode(img_file.read()).decode("utf-8")

# HIGH-ENERGY 4D CYBER STYLING FOR MATCHMINDAI
st.markdown(f"""
<head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&family=Space+Grotesk:wght@600;700&display=swap">
</head>
<style>
    /* Hide Streamlit Top Header */
    header, [data-testid="stHeader"], .stAppHeader {{
        background-color: #030712 !important;
        background: #030712 !important;
    }}

    /* Reduce Top Padding */
    .block-container {{
        padding-top: 0.8rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }}

    /* Global App Container */
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #030712 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.15) 0px, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(99, 102, 241, 0.18) 0px, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(245, 158, 11, 0.12) 0px, transparent 50%) !important;
        font-family: 'Outfit', sans-serif !important;
        color: #f8fafc !important;
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(16, 185, 129, 0.25) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #f8fafc !important;
    }}

    /* HERO BANNER FOR MATCHMINDAI */
    .hero-4d {{
        position: relative;
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 28px;
        border: 2px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9), 0 0 40px rgba(16, 185, 129, 0.3);
        background: #0b0f19;
    }}
    .hero-video-bg {{
        width: 100%;
        height: 250px;
        object-fit: cover;
        opacity: 0.65;
        filter: contrast(1.15) brightness(0.85);
    }}
    .hero-4d-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, rgba(3, 7, 18, 0.95) 0%, rgba(11, 15, 25, 0.55) 50%, rgba(3, 7, 18, 0.95) 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 40px;
    }}
    .hero-4d-tag {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(16, 185, 129, 0.18);
        border: 1.5px solid rgba(16, 185, 129, 0.5);
        color: #34d399;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 1px;
        width: fit-content;
        margin-bottom: 10px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }}
    .hero-4d-title {{
        font-size: 3.2rem;
        font-weight: 900;
        letter-spacing: -1.5px;
        background: linear-gradient(90deg, #34d399 0%, #38bdf8 40%, #a78bfa 75%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-transform: uppercase;
    }}
    .hero-4d-subtitle {{
        color: #cbd5e1;
        font-size: 1.15rem;
        font-weight: 600;
        margin-top: 6px;
    }}

    /* GLASS CARDS */
    .card-4d {{
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(11, 15, 25, 0.85) 100%);
        backdrop-filter: blur(20px);
        border: 1.5px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.7);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .card-4d:hover {{
        transform: translateY(-6px) scale(1.01);
        border-color: rgba(52, 211, 153, 0.7);
        box-shadow: 0 16px 50px rgba(16, 185, 129, 0.4);
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background: rgba(11, 15, 25, 0.9);
        padding: 8px;
        border-radius: 14px;
        border: 1.5px solid rgba(16, 185, 129, 0.3);
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 48px;
        border-radius: 10px;
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        background-color: transparent !important;
        border: none !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 25px rgba(16, 185, 129, 0.6) !important;
    }}

    /* Chat Messages & High Contrast Inputs */
    [data-testid="stChatMessage"] {{
        background-color: rgba(15, 23, 42, 0.95) !important;
        border: 1.5px solid rgba(16, 185, 129, 0.35) !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px !important;
    }}
    [data-testid="stChatMessage"] *, .stMarkdown p {{
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.65 !important;
    }}
    [data-testid="stChatInput"] {{
        background-color: #0b0f19 !important;
        border: 2px solid #10b981 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 25px rgba(16, 185, 129, 0.4) !important;
    }}
    [data-testid="stChatInput"] textarea, [data-testid="stChatInput"] input {{
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        -webkit-text-fill-color: #ffffff !important;
    }}
    div[data-baseweb="select"] > div, input, textarea {{
        background-color: #0b0f19 !important;
        color: #ffffff !important;
        border-color: rgba(16, 185, 129, 0.4) !important;
        -webkit-text-fill-color: #ffffff !important;
    }}
    div[data-baseweb="select"] * {{
        color: #ffffff !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(90deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        border: none !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.5) !important;
    }}
    .stButton > button:hover {{
        background: linear-gradient(90deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.8) !important;
        transform: translateY(-2px) !important;
    }}

    /* Metric Display */
    [data-testid="stMetricValue"] {{
        font-size: 2.3rem !important;
        font-weight: 900 !important;
        color: #34d399 !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-weight: 700 !important;
        color: #cbd5e1 !important;
    }}
</style>
""", unsafe_allow_html=True)

# 4D PARALLAX DEPTH PARTICLE ENGINE
components.html("""
<canvas id="canvas4d" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:999999;"></canvas>
<script>
    const canvas = document.getElementById('canvas4d');
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    const particles = [];
    const colors = ['#10b981', '#34d399', '#38bdf8', '#fbbf24', '#a78bfa'];
    
    class Particle4D {
        constructor(x, y) {
            this.x = x;
            this.y = y;
            this.z = Math.random() * 5 + 1;
            this.size = (Math.random() * 6 + 2) * (this.z / 3);
            this.speedX = (Math.random() - 0.5) * 3;
            this.speedY = (Math.random() - 0.5) * 3;
            this.color = colors[Math.floor(Math.random() * colors.length)];
            this.alpha = 1;
            this.decay = Math.random() * 0.025 + 0.015;
        }
        update() {
            this.x += this.speedX * (this.z / 2);
            this.y += this.speedY * (this.z / 2);
            this.alpha -= this.decay;
            if (this.size > 0.2) this.size -= 0.1;
        }
        draw() {
            ctx.save();
            ctx.globalAlpha = this.alpha;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 20 * (this.z / 2);
            ctx.shadowColor = this.color;
            ctx.fill();
            ctx.restore();
        }
    }
    
    window.addEventListener('mousemove', (e) => {
        for (let i = 0; i < 5; i++) {
            particles.push(new Particle4D(e.clientX, e.clientY));
        }
    });
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            if (particles[i].alpha <= 0 || particles[i].size <= 0.2) {
                particles.splice(i, 1);
                i--;
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
</script>
""", height=0, width=0)

# HERO BANNER FOR MATCHMINDAI
st.markdown(f"""
<div class="hero-4d">
    <video autoplay loop muted playsinline class="hero-video-bg">
        <source src="https://assets.mixkit.co/videos/preview/mixkit-stadium-lights-shining-at-night-42861-large.mp4" type="video/mp4">
        <img src="data:image/jpeg;base64,{stadium_b64}" class="hero-video-bg" alt="Stadium">
    </video>
    <div class="hero-4d-overlay">
        <div class="hero-4d-tag">
            <span>● LIVE REAL-TIME RADAR CONNECTED</span> • 10,000 MONTE CARLO RUNS ACTIVE
        </div>
        <h1 class="hero-4d-title">MatchMindAi</h1>
        <div class="hero-4d-subtitle">
            Real-Time Web Intelligence & 10,000-Run Monte Carlo Ball-by-Ball Simulation Engine
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 10px 0;">
        <div style="font-size: 3rem; margin-bottom: 5px;">⚡</div>
        <h2 style="color: #34d399; font-weight: 900; margin:0;">MatchMindAi</h2>
        <p style="color: #cbd5e1; font-size: 0.85rem;">Agentic Cricket Platform v4.0</p>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    st.markdown("""
    #### 🤖 System Capabilities
    - ⚡ **MatchMindAi Engine**: Real-time web scraper & player lookup.
    - 🎲 **10,000 Monte Carlo Runs**: Ball-by-ball stochastic match simulations.
    - 📊 **RandomForest ML Model**: Historical pattern matching.
    - ✨ **4D Depth Particle Radar**: Cursor motion tracking.
    """)
    st.divider()
    st.info("💡 Type your question below to get real-time answers from MatchMindAi!")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "💬 Ask MatchMindAi (Real-Time Access)", 
    "⚡ 1-Click Match Predictor", 
    "📰 Live Sports Intelligence Hub"
])

# ==========================================
# TAB 1: AI CHATBOT (MATCHMINDAI)
# ==========================================
with tab1:
    st.markdown("### 💬 Ask MatchMindAi (Real-Time Live Access)")
    st.caption("Ask MatchMindAi *any* question regarding player teams, match predictions, or pitch reports!")

    col_p1, col_p2, col_p3 = st.columns(3)
    preset_prompt = None
    
    with col_p1:
        if st.button("🏏 In which team does Virat Kohli play?"):
            preset_prompt = "In which team does Virat Kohli play?"
    with col_p2:
        if st.button("🏆 Who won Orange Cap in 2017?"):
            preset_prompt = "Who won Orange Cap in 2017?"
    with col_p3:
        if st.button("🏟️ Pitch & Weather Report for Wankhede"):
            preset_prompt = "What is the pitch report for Wankhede Stadium today?"

    st.markdown("<br>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Welcome! I am **MatchMindAi**, your real-time sports intelligence assistant. Ask me anything about cricket player teams, today's match predictions, or pitch reports!"
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "web_sources" in msg and msg["web_sources"]:
                with st.expander("🌐 View Real-Time Live Web Search Context"):
                    st.text(msg["web_sources"])

    user_input = st.chat_input("Ask MatchMindAi a question (e.g. In which team does Virat Kohli play?)...")
    prompt_to_process = preset_prompt if preset_prompt else user_input

    if prompt_to_process:
        st.session_state.messages.append({"role": "user", "content": prompt_to_process})
        with st.chat_message("user"):
            st.markdown(prompt_to_process)

        with st.chat_message("assistant"):
            with st.spinner("MatchMindAi is searching real-time web data..."):
                answer, live_web_data = answer_user_chatbot_query(prompt_to_process)
                st.markdown(answer)
                with st.expander("🌐 View Real-Time Live Web Search Context"):
                    st.text(live_web_data)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "web_sources": live_web_data
        })


# ==========================================
# TAB 2: EASY 1-CLICK MATCH PREDICTOR
# ==========================================
with tab2:
    st.markdown("### ⚡ MatchMindAi Match Predictor & 10,000 Simulator")
    st.caption("Select two teams and stadium venue to execute 10,000 stochastic ball-by-ball match simulations.")

    team_list = sorted(list(TEAM_RATINGS.keys()))
    venue_list = sorted(list(VENUE_PROFILES.keys()))
    
    col_t1, col_t2, col_v = st.columns(3)
    with col_t1:
        team1 = st.selectbox("Batting Team 1", team_list, index=team_list.index("Chennai Super Kings") if "Chennai Super Kings" in team_list else 0)
    with col_t2:
        team2 = st.selectbox("Bowling Team 2", team_list, index=team_list.index("Mumbai Indians") if "Mumbai Indians" in team_list else 1)
    with col_v:
        venue = st.selectbox("Stadium Venue", venue_list, index=venue_list.index("Wankhede Stadium") if "Wankhede Stadium" in venue_list else 0)
        
    col_tw, col_td, col_sim = st.columns(3)
    with col_tw:
        toss_winner = st.selectbox("Toss Winner", [team1, team2], index=0)
    with col_td:
        toss_decision = st.selectbox("Toss Decision", ["field", "bat"], index=0)
    with col_sim:
        n_sims = st.select_slider("Monte Carlo Iterations", options=[1000, 5000, 10000], value=10000)

    run_sim_btn = st.button("⚡ EXECUTE 10,000-RUN MONTE CARLO PREDICTION")

    if run_sim_btn:
        if team1 == team2:
            st.error("Please select two different teams.")
        else:
            with st.spinner("MatchMindAi is running 10,000 ball-by-ball simulations & scraping live web data..."):
                res = predict_full_match_agentic(team1, team2, venue, toss_winner, toss_decision, n_sims)
                
            st.success(f"✅ Prediction Complete: **{res['final_winner']}** predicted to win!")
            
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            with m_col1:
                st.metric("Predicted Winner", res["final_winner"], f"{res['final_win_prob']}% Win Probability")
            with m_col2:
                st.metric(f"{team1} Avg Score", f"{res['mc_results']['t1_avg_score']} Runs", f"{res['final_t1_pct']}% Win Chance")
            with m_col3:
                st.metric(f"{team2} Avg Score", f"{res['mc_results']['t2_avg_score']} Runs", f"{res['final_t2_pct']}% Win Chance")
            with m_col4:
                st.metric("Monte Carlo Runs", f"{n_sims:,} Matches", "Stochastic Simulation")

            st.markdown("<br>", unsafe_allow_html=True)

            c_col1, c_col2 = st.columns([1, 1])
            with c_col1:
                st.markdown("#### Win Probability Meter")
                gauge_fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=res["final_win_prob"],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"Predicted Winner: <b>{res['final_winner']}</b>", 'font': {'size': 16, 'color': '#ffffff'}},
                    number={'suffix': "%", 'font': {'size': 36, 'color': '#34d399'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#ffffff"},
                        'bar': {'color': "#10b981"},
                        'bgcolor': "#0b0f19",
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                            {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                        ],
                    }
                ))
                gauge_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=280, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(gauge_fig, use_container_width=True)

            with c_col2:
                st.markdown("#### 10,000-Run Score Distribution")
                t1_scores = res["mc_results"]["t1_scores_dist"]
                t2_scores = res["mc_results"]["t2_scores_dist"]
                dist_df = pd.DataFrame({
                    "Score": t1_scores + t2_scores,
                    "Team": [team1]*len(t1_scores) + [team2]*len(t2_scores)
                })
                fig_dist = px.histogram(dist_df, x="Score", color="Team", barmode="overlay", nbins=40, color_discrete_map={team1: "#34d399", team2: "#fbbf24"}, opacity=0.75)
                fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#0b0f19', font={'color': "white"}, height=280, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_dist, use_container_width=True)

            st.markdown("### 📝 AI Tactical Commentary Report")
            st.markdown(f"<div class='card-4d'>{res['match_report']}</div>", unsafe_allow_html=True)


# ==========================================
# TAB 3: LIVE SPORTS RADAR
# ==========================================
with tab3:
    st.markdown("### 📰 Live Sports & News Intelligence Hub")
    col_n1, col_n2 = st.columns([2, 1])
    with col_n1:
        st.markdown("#### 🔍 Real-Time News Search")
        search_query = st.text_input("Enter search topic:", value="IPL 2026 latest news")
        if st.button("Search Real-Time News"):
            with st.spinner("Fetching live Google News RSS data..."):
                results = search_realtime(search_query, max_results=6)
            if results:
                for item in results:
                    st.markdown(f"""
                    <div class="card-4d" style="padding:16px;">
                        <h4 style="color:#34d399; margin:0 0 6px 0;">{item['title']}</h4>
                        <p style="font-size:0.9rem; color:#cbd5e1; margin:0;">{item['snippet']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    with col_n2:
        st.markdown("#### 📊 Venue Pitch Profiles")
        venue_df = pd.DataFrame([{"Venue": v, "Avg Score": d["avg_score"], "Dew Factor": d["dew_factor"]} for v, d in VENUE_PROFILES.items()])
        st.dataframe(venue_df, use_container_width=True, hide_index=True)