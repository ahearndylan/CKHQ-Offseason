import tweepy
import random
import time
from datetime import datetime

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
#     TRIVIA QUESTIONS    #
# ======================= #

TRIVIA_QUESTIONS = [
    {
        "question": "Who is the only player in NBA history with a 20-assist triple-double in a playoff game?",
        "answer": "Magic Johnson"
    },
    {
        "question": "Which player recorded the only 30-point, 10-block game in the playoffs since 2000?",
        "answer": "Dwight Howard"
    },
    {
        "question": "Who is the youngest player to record a triple-double in NBA playoff history?",
        "answer": "Magic Johnson"
    },
    {
        "question": "Which player had the most steals in a single NBA playoff game?",
        "answer": "Allen Iverson"
    },
    {
        "question": "Who was the last player to average at least 35 PPG in a single postseason (min 10 games)?",
        "answer": "Luka Doncic"
    },
    {
        "question": "Which player recorded a 45-point game while shooting 70 percent+ in a playoff loss?",
        "answer": "Giannis Antetokounmpo"
    },
    {
        "question": "Who is the only player with a 40-point game off the bench in NBA playoff history?",
        "answer": "Nick Van Exel"
    },
    {
        "question": "Which player has the most playoff games with 5+ steals since 2000?",
        "answer": "Dwyane Wade"
    },
    {
        "question": "Who recorded the most blocks in a single NBA Finals game?",
        "answer": "Dwight Howard"
    },
    {
        "question": "Which player had a 25-rebound game in the 2023 NBA Playoffs?",
        "answer": "Kevon Looney"
    },
    {
        "question": "Which player recorded back-to-back 40-point games in the 2022 NBA Playoffs?",
        "answer": "Luka Doncic"
    },
    {
        "question": "Who is the only player with a triple-double in their NBA Finals debut?",
        "answer": "Jason Kidd"
    },
    {
        "question": "Who scored the most points in their first ever NBA playoff game?",
        "answer": "John Williamson"
    },
    {
        "question": "Which player has the most career playoff games with 30+ points and 10+ assists?",
        "answer": "LeBron James"
    },
    {
        "question": "Who is the only player with a playoff game of 25+ points, 15+ assists, and 0 turnovers?",
        "answer": "Chris Paul"
    },
    {
        "question": "Which player is the only center with 15+ assists in a modern era playoff game?",
        "answer": "Nikola Jokic"
    },
    {
        "question": "Who holds the record for most three-pointers made in a single NBA Finals game?",
        "answer": "Stephen Curry"
    },
    {
        "question": "Who is the oldest player to record a triple-double in a playoff game?",
        "answer": "LeBron James"
    },
    {
        "question": "Which player had the most 40+ point games in a single postseason?",
        "answer": "Michael Jordan"
    },
    {
        "question": "Which player recorded a 30-10-10 playoff triple-double while hitting 7+ threes?",
        "answer": "James Harden"
    }
]


# ======================= #
#     TWEET FORMATTER     #
# ======================= #

def build_tweet(question_text):
    return (
        "🏀 COURT KINGS TRIVIA 👑\n\n"
        f"{question_text}\n\n"
        "Reply with your guess ⬇️\n\n"
        "#NBATrivia #CourtKingsHQ"
    )

# ======================= #
#       POST TRIVIA       #
# ======================= #

def post_trivia():
    trivia = random.choice(TRIVIA_QUESTIONS)
    tweet_text = build_tweet(trivia["question"])

    try:
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data["id"]
        print("✅ Trivia posted!")
        print("📊 Question:", trivia["question"])
        print("🔐 Answer:", trivia["answer"])
        return tweet_id
    except Exception as e:
        print("❌ Failed to post trivia:", e)
        return None

# ======================= #
#    LIKE REPLIES LATER   #
# ======================= #

def like_replies_to(tweet_id, delay=60):
    print(f"⏳ Waiting {delay} seconds before checking for replies...")
    time.sleep(delay)

    try:
        # Get replies by searching for tweets that mention @StatKingsHQ AND are replying to tweet_id
        query = f"to:StatKingsHQ conversation_id:{tweet_id} -is:retweet"
        response = client.search_recent_tweets(
            query=query,
            max_results=20,
            tweet_fields=["in_reply_to_user_id"]
        )
        if not response.data:
            print("😶 No replies found yet.")
            return

        for tweet in response.data:
            try:
                client.like(tweet.id)
                print(f"💙 Liked reply: {tweet.id}")
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error liking tweet {tweet.id}: {e}")

    except Exception as e:
        print("❌ Failed to fetch replies:", e)

# ======================= #
#        MAIN BOT         #
# ======================= #

def run_trivia_bot():
    print(f"🚀 Running Stat Kings Trivia Bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tweet_id = post_trivia()
    if tweet_id:
        like_replies_to(tweet_id, delay=90)

if __name__ == "__main__":
    run_trivia_bot()
