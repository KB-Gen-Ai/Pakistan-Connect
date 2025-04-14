import pandas as pd
import os

DB_FILE = "data/profiles.csv"

def save_profile(data: dict):
    df = pd.DataFrame([data])

    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(DB_FILE):
        existing = pd.read_csv(DB_FILE, dtype=str)
        if data["email"] in existing["email"].values or data["phone"] in existing["phone"].values:
            return  # Duplicate found

        combined = pd.concat([existing, df], ignore_index=True)
    else:
        combined = df

    combined.to_csv(DB_FILE, index=False)

def get_profile_by_id(profile_id: str):
    try:
        df = pd.read_csv(DB_FILE, dtype=str)
        profile = df[df["id"] == profile_id]
        if not profile.empty:
            return profile.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None
