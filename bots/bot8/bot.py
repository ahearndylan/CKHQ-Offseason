import json
import tweepy
from supabase import create_client, Client

# === Supabase Config ===
supabase_url = "https://fjtxowbjnxclzcogostk.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZqdHhvd2JqbnhjbHpjb2dvc3RrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI2MDE5NTgsImV4cCI6MjA1ODE3Nzk1OH0.LPkFw-UX6io0F3j18Eefd1LmeAGGXnxL4VcCLOR_c1Q"  # full key here
supabase: Client = create_client(supabase_url, supabase_key)

def load_category_state():
    res = supabase.table("categorystate").select("category_index").eq("id", 1).execute()
    if res.data and len(res.data) > 0:
        return res.data[0]["category_index"]
    else:
        supabase.table("categorystate").insert({"id": 1, "category_index": 1}).execute()
        return 1

def save_category_state(index):
    supabase.table("categorystate").update({"category_index": index}).eq("id", 1).execute()

# === Twitter Auth ===
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPztzwEAAAAAvBGCjApPNyqj9c%2BG7740SkkTShs%3DTCpOQ0DMncSMhaW0OA4UTPZrPRx3BHjIxFPzRyeoyMs2KHk6hM"
api_key = "uKyGoDr5LQbLvu9i7pgFrAnBr"
api_secret = "KGBVtj1BUmAEsyoTmZhz67953ItQ8TIDcChSpodXV8uGMPXsoH"
access_token = "1901441558596988929-WMdEPOtNDj7QTJgLHVylxnylI9ObgD"
access_token_secret = "9sf83R8A0MBdijPdns6nWaG7HF47htcWo6oONPmMS7o98"

client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# === Categories in rotation ===
categories = [
    "points", "rebounds", "assists", "steals", "blocks",
    "3pm", "triple_doubles", "minutes", "games", "mvps"
]

def load_leaderboard_data():
    with open("leaders_data.json", "r") as f:
        return json.load(f)

def create_tweet(category, leaders):
    title_map = {
        "points": "All-Time Points",
        "rebounds": "All-Time Rebounds",
        "assists": "All-Time Assists",
        "steals": "All-Time Steals",
        "blocks": "All-Time Blocks",
        "3pm": "All-Time 3PM Made",
        "triple_doubles": "All-Time Triple-Doubles",
        "minutes": "Most Minutes Played",
        "games": "Most Games Played",
        "mvps": "Most MVP Awards"
    }

    title = title_map[category]
    tweet = f"⚔️ Battle for the Crown – NBA {title} 👑\n\n"

    for i, name in enumerate(leaders):
        prefix = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i + 1}."
        tweet += f"{prefix} {name}\n"

    tweet += "\n#NBA #CourtKingsHQ"
    return tweet

def main():
    category_index = load_category_state()
    category = categories[category_index - 1]

    data = load_leaderboard_data()
    leaders = data[category]

    tweet = create_tweet(category, leaders)
    print(tweet)

    try:
        client.create_tweet(text=tweet)
        print("✅ Tweet posted!")
    except Exception as e:
        print("❌ Failed to tweet:", e)

    next_category = category_index + 1 if category_index < len(categories) else 1
    save_category_state(next_category)

if __name__ == "__main__":
    main()
