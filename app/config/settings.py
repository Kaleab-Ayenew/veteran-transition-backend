from dotenv import load_dotenv
import os
load_dotenv(override=True)

DB_URL=os.environ.get("DB_URL")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
NAVY_CAREER_MAIN_PAGE=os.environ.get("NAVY_CAREER_MAIN_PAGE")
ANT_SCRAPER_KEY=os.environ.get("ANT_SCRAPER_KEY")
CSS_FILE_PATH=os.environ.get("CSS_FILE_PATH")
GENERATED_RESUME_PATH=os.environ.get("GENERATED_RESUME_PATH")
BACKEND_BASE_URL=os.environ.get("BACKEND_BASE_URL")