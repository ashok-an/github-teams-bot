import os

from dotenv import load_dotenv
load_dotenv()

bot_email = os.getenv("TEAMS_BOT_EMAIL")
teams_token = os.getenv("TEAMS_BOT_TOKEN")
bot_url = os.getenv("TEAMS_BOT_URL")
bot_app_name = os.getenv("TEAMS_BOT_APP_NAME")
search_engine_api_key = os.getenv("API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")

if __name__ == '__main__':
    print(bot_email, teams_token, bot_url, bot_app_name)
