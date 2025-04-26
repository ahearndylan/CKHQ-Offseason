import json
import tweepy

# === Twitter Auth === #
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

# === Categories in rotation === #
categories = [
    "points", "rebounds", "assists", "steals", "blocks",
    "3pm", "triple_doubles", "minutes", "games", "mvps"
]

def load_category_state():
    with open("category_state.json", "r") as f:
        return json.load(f)["category"]

def save_category_state(next_cat):
    with open("category_state.json", "w") as f:
        json.dump({ "category": next_cat }, f)

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

    medals = ["🥇", "🥈", "🥉"]
    for i, name in enumerate(leaders):
        if i == 0:
            prefix = "🥇"
        elif i == 1:
            prefix = "🥈"
        elif i == 2:
            prefix = "🥉"
        else:
            prefix = f"{i + 1}."
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
