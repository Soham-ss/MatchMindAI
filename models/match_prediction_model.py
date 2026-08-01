import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


# Load Dataset
df = pd.read_csv("dataset/IPL.csv", low_memory=False)


# Select required columns
df = df[
    [
        "batting_team",
        "bowling_team",
        "venue",
        "toss_winner",
        "toss_decision",
        "match_won_by"
    ]
]


# Remove missing values
df = df.dropna()


# Encode categorical columns
le_batting = LabelEncoder()
le_bowling = LabelEncoder()
le_venue = LabelEncoder()
le_toss_winner = LabelEncoder()
le_toss_decision = LabelEncoder()
le_winner = LabelEncoder()


df["batting_team"] = le_batting.fit_transform(df["batting_team"])
df["bowling_team"] = le_bowling.fit_transform(df["bowling_team"])
df["venue"] = le_venue.fit_transform(df["venue"])
df["toss_winner"] = le_toss_winner.fit_transform(df["toss_winner"])
df["toss_decision"] = le_toss_decision.fit_transform(df["toss_decision"])
df["match_won_by"] = le_winner.fit_transform(df["match_won_by"])


# Features
X = df.drop("match_won_by", axis=1)

# Target
y = df["match_won_by"]


# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Train Model
model = RandomForestClassifier()

model.fit(X_train, y_train)


# Check Accuracy
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy :", accuracy)


# Save Model
# Save ML Model
joblib.dump(model, "models/match_predictor.pkl")


# Save Label Encoders
joblib.dump(le_batting, "models/batting_encoder.pkl")
joblib.dump(le_bowling, "models/bowling_encoder.pkl")
joblib.dump(le_venue, "models/venue_encoder.pkl")
joblib.dump(le_toss_winner, "models/toss_winner_encoder.pkl")
joblib.dump(le_toss_decision, "models/toss_decision_encoder.pkl")
joblib.dump(le_winner, "models/winner_encoder.pkl")


print("\nEverything Saved Successfully!")