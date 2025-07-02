import json
import os
import random
import tweepy
from time import sleep

# ======================= #
# TWITTER AUTHENTICATION  #
# ======================= #
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

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api_v1 = tweepy.API(auth)

# ======================= #
#   FILE PATH SETUP       #
# ======================= #

base_dir = os.path.dirname(os.path.abspath(__file__))
players_file_path = os.path.join(base_dir, "players.json")
stats_file_path = os.path.join(base_dir, "players_stats.json")
img_dir = os.path.join(base_dir, "img")

# ======================= #
#   FILE LOAD/SAVE FUNC   #
# ======================= #

def load_players():
    with open(players_file_path, "r") as f:
        return json.load(f)

def save_players(players_list):
    with open(players_file_path, "w") as f:
        json.dump(players_list, f, indent=2)

def load_stats():
    with open(stats_file_path, "r") as f:
        return json.load(f)

# ======================= #
#     TWEET GENERATION    #
# ======================= #

def generate_tweet(player_stat):
    return (
        f"👑 Rookie Royalty – {player_stat['name']}\n\n"
        f"📅 Season: {player_stat['season']} ({player_stat['team']})\n"
        f"🚀 Stats: {player_stat['ppg']} PPG · {player_stat['rpg']} RPG · {player_stat['apg']} APG · {player_stat['fg_pct']}% FG\n"
        f"🕹️ Games Played: {player_stat['games_played']}\n\n"
        f"#NBA #NBAStats #CourtKingsHQ"
    )

def post_tweet(text, image_file=None):
    try:
        if image_file:
            image_path = os.path.join(img_dir, image_file)
            print(f"📷 Trying image: {image_path}")
            if os.path.exists(image_path):
                media = api_v1.media_upload(filename=image_path)
                client.create_tweet(text=text, media_ids=[media.media_id_string])
                print(f"✅ Tweet posted with image: {image_file}")
            else:
                print(f"⚠️ Image not found: {image_path}. Posting without image.")
                client.create_tweet(text=text)
        else:
            client.create_tweet(text=text)
            print("✅ Tweet posted without image.")
    except Exception as e:
        print("❌ Tweet failed:", e)

# ======================= #
#         MAIN BOT        #
# ======================= #

def main():
    players_list = load_players()
    stats_list = load_stats()
    unused_players = [p for p in players_list if not p.get("used")]

    if not unused_players:
        print("✅ All players have been used.")
        return

    selected = random.choice(unused_players)
    player_name = selected["name"]

    # Find matching stat entry
    stat_entry = next((s for s in stats_list if s["name"] == player_name), None)

    if not stat_entry:
        print(f"❌ No stats found for {player_name}")
        return

    tweet = generate_tweet(stat_entry)
    print("\n" + tweet)

    post_tweet(tweet, image_file=selected.get("image", None))

    # Mark player as used
    for p in players_list:
        if p["name"] == player_name:
            p["used"] = True
            break

    save_players(players_list)
    sleep(1)

if __name__ == "__main__":
    main()
