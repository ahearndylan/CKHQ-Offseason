import json
import random
import tweepy
import os

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

# === Draft Bot Config === #
base_dir = os.path.dirname(__file__)
FILE_PATH = os.path.join(base_dir, "draft_picks.json")

def load_draft_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_draft_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def get_unused_pick(data):
    unused = [p for p in data if not p.get("used", False)]
    if not unused:
        print("✅ All players have been used.")
        return None
    return random.choice(unused)

def format_tweet(player):
    return (
        f"👑 Draft Royalty\n"
        f"📅 {player['year']} NBA Draft | #{player['pick']} Pick\n\n"
        f"{player['player']} to the {player['team']}\n"
        f"{player['career']}\n\n"
        f"#NBADraft #CourtKingsHQ"
    )

def main():
    print("🤖 Running Court Kings Draft Throwback Bot...\n")

    data = load_draft_data()
    pick = get_unused_pick(data)

    if pick:
        tweet = format_tweet(pick)
        print(tweet)

        # Tweet it out
        try:
            client.create_tweet(text=tweet)
            print("✅ Tweet posted!")
        except Exception as e:
            print("❌ Failed to tweet:", e)

        # Mark player as used
        for p in data:
            if p["player"] == pick["player"] and p["year"] == pick["year"]:
                p["used"] = True
                break

        save_draft_data(data)
    else:
        print("🎉 All entries used. Add more players to the file to continue.")

if __name__ == "__main__":
    main()
