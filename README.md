# ⚡ MatchMindAi - Real-Time Cricket Intelligence & 10,000-Run Monte Carlo Simulation Engine

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-RandomForest-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Deploy](https://img.shields.io/badge/Live-App_Deployed-10b981?style=for-the-badge)

- 🌐 **Live Web Application**: [matchmindai-t5mgmcv6r79nflpye5ykla.streamlit.app](https://matchmindai-t5mgmcv6r79nflpye5ykla.streamlit.app)
- 📦 **GitHub Repository**: [github.com/Soham-ss/MatchMindAI](https://github.com/Soham-ss/MatchMindAI)
- 📄 **PDF Presentation Deck**: [MatchMindAi_Presentation.pdf](./MatchMindAi_Presentation.pdf)
- 🌐 **Printable HTML Deck**: [MatchMindAi_Presentation.html](./MatchMindAi_Presentation.html)

---

## 📌 Project Overview

**MatchMindAi** is an advanced cricket intelligence and match prediction platform. It combines **Machine Learning (RandomForest)**, **10,000-Run Monte Carlo Ball-by-Ball Simulations**, **Real-Time Web Intelligence Scrapers**, and an **18-Year Historical IPL Knowledge Engine (2008–2026)** into a high-energy 4D cyber dashboard.

---

## 📊 10-Slide Presentation Deck (PPT Layout)

### 📌 Slide 1: Introduction & Overview
- **Core Goal**: Provide cricket fans and analysts with 10,000 ball-by-ball simulated match predictions and instant 1-line factual answers for all 18 IPL seasons (2008–2026).
- **Tech Stack**: Python 3.14, Streamlit, Scikit-Learn, Plotly, NumPy, Pandas, BeautifulSoup4, HTML5/CSS3.

---

### ❓ Slide 2: The Problem We Solved
- ❌ **Static Historical Data Only**: Old prediction tools ignore today's live pitch reports, weather updates, and stadium dew factors.
- ❌ **Messy AI Data Dumps**: General AI chatbots return long, messy URL links (`Source [1]...`) instead of simple 1-line answers.
- ❌ **Lack of Match Simulation**: Fans cannot simulate thousands of ball-by-ball match scenarios to view score distribution ranges.

---

### 🚀 Slide 3: Our Solution (MatchMindAi)
- ⚡ **10,000-Run Monte Carlo Simulation Engine**: Simulates 10,000 ball-by-ball matches per click based on team ratings, venue pitch profiles, and dew factors.
- 🏆 **1-Line Direct Factual Answers**: Instantly answers player team queries, Orange Cap winners, Purple Cap winners, and Champions for any year (2008–2026).
- 🌐 **Real-Time Web Intelligence**: Scrapes live Google News RSS feeds to incorporate today's pitch, weather, and team squad updates.
- ✨ **High-Energy 4D Cyber UI**: Dark mode aesthetic, live stadium video header, cursor depth particle radar, and sticky bottom Chat Box.

---

### ✨ Slide 4: Main Platform Features
- 💬 **Smart AI Chatbot**: Recognizes user introductions personally (*"Hi my name is Soham"* ➔ *"Hello Soham! 👋"*).
- 🏆 **18-Year IPL Database**: Maps every Orange Cap, Purple Cap, and Champion from 2008 to 2025 (e.g. David Warner 2017: 641 runs).
- ⚠️ **Pre-2008 Boundary Check**: Detects invalid pre-2008 queries (*"who won in 2005"*) explaining IPL was founded in 2008 with Shaun Marsh.
- ⚡ **1-Click Match Predictor**: Pick 2 teams and a stadium venue to generate win probability meters and score histogram graphs.

---

### 🏗️ Slide 5: System Architecture & Workflow

```text
               [ 👤 User Prompt / Selection ]
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
  [ 💬 Chatbot Intent Router ]   [ ⚡ Match Predictor ]
             │                           │
  ├── 18-Year IPL Dictionary     ├── 🌐 Real-Time Scraper (Google News)
  ├── Pre-2008 Check           ├── 🎲 10,000 Monte Carlo Simulations
  └── Name Recognition Engine    └── 📊 RandomForest ML Classifier
             │                           │
             └─────────────┬─────────────┘
                           ▼
            [ 🎨 High-Energy 4D Cyber UI ]
```

1. **Step 1 (User Input)**: User enters a question or selects 2 teams & stadium venue.
2. **Step 2 (Intent Router)**: Classifies query into Greeting, Bot Identity, IPL History Lookup, or Match Prediction.
3. **Step 3 (Parallel Sub-Agents)**: Web Scraper Agent + Monte Carlo Simulator + RandomForest ML Model.
4. **Step 4 (Ensemble Blend)**: Combines 55% Monte Carlo + 45% ML to compute final win probabilities.
5. **Step 5 (Streamlit UI)**: Renders win gauges, score graphs, and crisp markdown commentary.

---

### 📊 Slide 6: Machine Learning & Simulation Details
- 📊 **RandomForest ML Classifier**: Trained on historical IPL datasets using `scikit-learn`. Pre-compiled weights are saved as `.pkl` binary files inside `models/`.
- 🎲 **Stochastic Monte Carlo Math**: Calculates run probabilities per ball based on team rating (CSK 88, MI 87, RCB 85) and venue dew factor (Wankhede 0.12).
- 📈 **Interactive Plotly Graphs**: Displays score distribution histograms showing expected run ranges across 10,000 simulated matches.

---

### ⚡ Slide 7: Technical Challenges Faced & Solved
- 🔴 **GitHub 100 MB Limit**: `git push` failed because `dataset/IPL.csv` was 104.93 MB.
  - ✅ **Solution**: Removed `IPL.csv` from git history because model weights were already compiled into `.pkl` binary files in `models/`.
- 🔴 **Streamlit Cloud Path Errors**: Relative paths like `"models/match_predictor.pkl"` crashed on Linux.
  - ✅ **Solution**: Replaced relative string paths with Python's `os.path.abspath` to dynamically locate exact folder paths.
- 🔴 **Missing Cloud Packages**: Missing `beautifulsoup4` and `python-dotenv` caused `ModuleNotFoundError`.
  - ✅ **Solution**: Added packages to `requirements.txt` and wrapped imports in safe `try...except` blocks.
- 🔴 **Phrasing Variations**: *"who wins 2018 ipl"* (present tense) bypassed *"who won"* router.
  - ✅ **Solution**: Expanded regex keywords to catch all tense variations (`"who wins"`, `"wins"`, `"win"`, `"won"`).

---

### 🎨 Slide 8: UI/UX & High-Energy Design System
- 🌌 **Cyberpunk Dark Aesthetic**: Designed with a sleek `#030712` background and HSL tailored emerald accents (`#10b981`, `#34d399`).
- 🔤 **Modern Typography**: Uses Google Font (`Outfit`) for maximum legibility across laptops, tablets, and mobile devices.
- 🎬 **Dynamic Visual FX**: Features a looping HD stadium lights video banner and an interactive 4D particle cursor depth radar.
- 📌 **Sticky Bottom Chat Input**: Pinned Chat Box stays permanently visible at the bottom of the viewport when scrolling long chat histories.

---

### 🌐 Slide 9: Cloud Deployment & Infrastructure
- ☁️ **Live Hosting**: Hosted live on **Streamlit Community Cloud** with 100% uptime at [matchmindai-t5mgmcv6r79nflpye5ykla.streamlit.app](https://matchmindai-t5mgmcv6r79nflpye5ykla.streamlit.app).
- 📦 **Source Control**: Version-controlled on **GitHub** ([github.com/Soham-ss/MatchMindAI](https://github.com/Soham-ss/MatchMindAI)).
- 🔄 **Automated CI/CD**: Pushing code updates to GitHub main branch automatically triggers a rebuild on Streamlit Cloud within ~30 seconds.

---

### 🔮 Slide 10: Conclusion & Future Scope
- 🏆 **Conclusion**: **MatchMindAi** successfully combines Artificial Intelligence, Machine Learning, Monte Carlo Simulations, and Real-Time Internet Scraping into a fast, accurate, and visually stunning web platform.
- 📡 **Live Score API Integration**: Connect live cricket APIs for real-time win probability shifts during active live matches.
- 🏏 **Fantasy Team Optimizer**: Auto-generate optimal Dream11 / My11Circle lineups based on Monte Carlo expected points.
- ⚽ **Multi-Sport Expansion**: Extend simulation models to Football (Premier League, Champions League) and Basketball (NBA).
