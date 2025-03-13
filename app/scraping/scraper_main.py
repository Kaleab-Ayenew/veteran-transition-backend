import json
from app.db import db_utils, models
from app.llm.open_ai import LLMClient
from app.llm import prompts
from app.scraping.scraping_ant import AntScraper

class MainPageScraper:
    def __init__(self):
        self.main_page_url = "https://www.navy.com/careers-benefits/careers"
        self.llm_client = LLMClient(model="gpt-4o-mini", history=[{"role": "system", "content": prompts.LINK_EXTRACTOR_SYSTEM_PROMPT}])
        self.scraping_agent = AntScraper(scrap_url=self.main_page_url,
                                         extract_type="markdown")
        self.extracted_positions = []
        
    def get_career_links(self) -> dict:
        """
            Returns dict of format:
                ```json
                    {
                    "military_positions": [
                        {
                            "title": "[Job Title]",
                            "category": "[Job Category]",
                            "details_url": "[URL for the job details]"
                        },
                        ...
                    ]
                    }
                ```
        """
        scraped_data = self.scraping_agent.get_content()
        markdown_text = scraped_data.get("markdown")
        extracted_data = self.llm_client.send_message(input=[{"role":"user", "content": markdown_text}], response_format="json_object")
        extracted_data = json.loads(extracted_data)
        self.extracted_positions = extracted_data
        return extracted_data
    
    def save_to_database(self):
        n = 0
        for pos in self.extracted_positions.get("military_positions"):
            if db_utils.filter_rows(model=models.MilitaryPosition, filters=(models.MilitaryPosition.url == pos.get("details_url"),)):
                continue
            n = n + 1
            new_position_entry = db_utils.create_row(model=models.MilitaryPosition, data={
                "name": pos.get("title"),
                "url": pos.get("details_url"),
                "category": pos.get("category")
            })
            print(f"[*] Created new military position entry: {new_position_entry.name}")
        print(f"[*] Saved {n} new military positions.")
        
    

if __name__ == "__main__":
    main_scraper = MainPageScraper()
    links = main_scraper.get_career_links()
    print(links)