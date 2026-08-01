import joblib
import pandas as pd
import numpy as np

# Load ML Model & Encoders with safety
try:
    model = joblib.load("models/match_predictor.pkl")
    batting_encoder = joblib.load("models/batting_encoder.pkl")
    bowling_encoder = joblib.load("models/bowling_encoder.pkl")
    venue_encoder = joblib.load("models/venue_encoder.pkl")
    toss_winner_encoder = joblib.load("models/toss_winner_encoder.pkl")
    toss_decision_encoder = joblib.load("models/toss_decision_encoder.pkl")
    winner_encoder = joblib.load("models/winner_encoder.pkl")
    HAS_ML_MODEL = True
except Exception as e:
    print(f"Warning: Could not load trained ML model ({e}). Using simulation mode.")
    HAS_ML_MODEL = False


def safe_encode(encoder, value, default_idx=0):
    """Encodes categorical string safely without raising ValueError for unseen labels."""
    if not hasattr(encoder, "classes_"):
        return default_idx
        
    classes = list(encoder.classes_)
    if value in classes:
        return encoder.transform([value])[0]
        
    # Search for substring or partial match
    for idx, cls_name in enumerate(classes):
        if str(value).lower() in str(cls_name).lower() or str(cls_name).lower() in str(value).lower():
            return idx
            
    # Default to first known class index if unseen
    return default_idx


def predict_match_ml(team1, team2, venue, toss_winner, toss_decision):
    """
    Predicts match winner using trained RandomForest ML Model + Label Encoders.
    """
    if not HAS_ML_MODEL:
        return team1, 55.0  # Default fallback if pkl is missing
        
    try:
        t1_code = safe_encode(batting_encoder, team1, 0)
        t2_code = safe_encode(bowling_encoder, team2, 1)
        v_code = safe_encode(venue_encoder, venue, 0)
        tw_code = safe_encode(toss_winner_encoder, toss_winner, 0)
        td_code = safe_encode(toss_decision_encoder, toss_decision, 0)
        
        data = pd.DataFrame([[
            t1_code,
            t2_code,
            v_code,
            tw_code,
            td_code
        ]], columns=[
            "batting_team",
            "bowling_team",
            "venue",
            "toss_winner",
            "toss_decision"
        ])
        
        pred_idx = model.predict(data)[0]
        probs = model.predict_proba(data)[0]
        max_prob = round(float(np.max(probs)) * 100, 2)
        
        winner_name = winner_encoder.inverse_transform([pred_idx])[0]
        return winner_name, max_prob
    except Exception as e:
        print(f"ML Prediction Error: {e}")
        return team1, 52.0


if __name__ == "__main__":
    w, p = predict_match_ml("Chennai Super Kings", "Mumbai Indians", "Wankhede Stadium", "Mumbai Indians", "field")
    print(f"ML Prediction Winner: {w} ({p}%)")