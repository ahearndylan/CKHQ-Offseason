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

# Tweepy v1.1 API for media uploads
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api_v1 = tweepy.API(auth)

# === File Paths === #
base_dir = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(base_dir, "draft_picks.json")
IMG_DIR = os.path.join(base_dir, "img")

# === Load and Save JSON === #
def load_draft_data():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_draft_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

# === Pick unused player === #
def get_unused_pick(data):
    unused = [p for p in data if not p.get("used", False)]
    if not unused:
        print("✅ All players have been used.")
        return None
    return random.choice(unused)

# === Format tweet text === #
def format_tweet(player):
    return (
        f"👑 Draft Royalty\n"
        f"📅 {player['year']} NBA Draft | #{player['pick']} Pick\n\n"
        f"{player['player']} to the {player['team']}\n"
        f"{player['career']}\n\n"
        f"#NBADraft #CourtKingsHQ"
    )

# === Main Bot Run === #
def main():
    print("🤖 Running Court Kings Draft Throwback Bot...\n")

    data = load_draft_data()
    pick = get_unused_pick(data)

    if not pick:
        print("🎉 All entries used. Add more players to the file to continue.")
        return

    tweet = format_tweet(pick)
    print(tweet)

    image_file = pick.get("image", "")
    image_path = os.path.join(IMG_DIR, image_file)

    try:
        if image_file and os.path.exists(image_path):
            media = api_v1.media_upload(filename=image_path)
            client.create_tweet(text=tweet, media_ids=[media.media_id_string])
            print(f"✅ Tweet posted with image: {image_file}")
        else:
            print(f"⚠️ No image found at: {image_path}")
            client.create_tweet(text=tweet)
            print("✅ Tweet posted without image.")

        # Mark as used
        for p in data:
            if p["player"] == pick["player"] and p["year"] == pick["year"]:
                p["used"] = True
                break

        save_draft_data(data)

    except Exception as e:
        print("❌ Failed to tweet:", e)

if __name__ == "__main__":
    main()
