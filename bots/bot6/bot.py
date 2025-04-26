import json
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from time import sleep
import tweepy
import os

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
#     PLAYER FUNCTIONS    #
# ======================= #

def load_players():
    with open("players.json", "r") as f:
        return json.load(f)

def save_players(players_list):
    with open("players.json", "w") as f:
        json.dump(players_list, f, indent=2)

def get_rookie_stats(player_name):
    found = players.find_players_by_full_name(player_name)
    if not found:
        print(f"❌ Player not found: {player_name}")
        return None

    player_id = found[0]["id"]
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
        rookie_row = career.iloc[0]

        pts = rookie_row["PTS"]
        reb = rookie_row["REB"]
        ast = rookie_row["AST"]
        gp = rookie_row["GP"]
        fg_pct = rookie_row["FG_PCT"]
        season = rookie_row["SEASON_ID"]
        team = rookie_row["TEAM_ABBREVIATION"]

        if gp == 0:
            print(f"⚠️ No games played for {player_name}")
            return None

        ppg = round(pts / gp, 1)
        rpg = round(reb / gp, 1)
        apg = round(ast / gp, 1)
        fg = round(fg_pct * 100, 1)

        tweet = (
            f"👑 Rookie Royalty – {player_name}\n\n"
            f"📅 Season: {season} ({team})\n"
            f"🚀 Stats: {ppg} PPG · {rpg} RPG · {apg} APG · {fg}% FG\n"
            f"🕹️ Games Played: {gp}\n\n"
            f"#NBA #NBAStats #CourtKingsHQ"
        )

        return tweet

    except Exception as e:
        print(f"⚠️ Failed to get stats for {player_name}: {e}")
        return None

def post_tweet(text):
    try:
        client.create_tweet(text=text)
        print("✅ Tweet posted.")
    except Exception as e:
        print("❌ Tweet failed:", e)

# ======================= #
#         MAIN BOT        #
# ======================= #

def main():
    players_list = load_players()
    for player in players_list:
        if not player["used"]:
            tweet = get_rookie_stats(player["name"])
            if tweet:
                print("\n" + tweet)
                post_tweet(tweet)
                player["used"] = True
                save_players(players_list)
            sleep(1)
            break  # Only one player per run

if __name__ == "__main__":
    main()
