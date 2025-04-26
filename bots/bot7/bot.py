import json
import random
import tweepy

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

# ======================= #
#     MAIN BOT LOGIC      #
# ======================= #

def load_players():
    with open("players.json", "r") as f:
        return json.load(f)

def create_debate_poll():
    all_players = load_players()
    selected = random.sample(all_players, 3)
    
    question = (
        f"⚔️ Battle for the Throne\n\n"
        f"Which of these legends had the most dominant prime?\n\n"
        f"👑 {selected[0]}\n"
        f"👑 {selected[1]}\n"
        f"👑 {selected[2]}\n\n"
        f"Vote below 👇 #NBA #CourtKingsHQ"
    )


    
    try:
        client.create_tweet(
            text=question,
            poll_options=selected,
            poll_duration_minutes=1440  # 24 hours
        )
        print("✅ Debate poll posted!")
    except Exception as e:
        print("❌ Failed to post poll:", e)

if __name__ == "__main__":
    create_debate_poll()
