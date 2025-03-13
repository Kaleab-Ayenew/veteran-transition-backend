from dotenv import load_dotenv
import os
load_dotenv()

DB_URL=os.environ.get("DB_URL")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
NAVY_CAREER_MAIN_PAGE=os.environ.get("NAVY_CAREER_MAIN_PAGE")
ANT_SCRAPER_KEY=os.environ.get("ANT_SCRAPER_KEY")