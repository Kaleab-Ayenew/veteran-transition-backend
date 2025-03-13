from app.scraping.scraper_main import MainPageScraper
from app.llm.translator import CareerTranslator
from app.scraping.scraping_ant import AntScraper



if __name__ == "__main__":
    main_page_scraper = MainPageScraper()
    career_translator = CareerTranslator()
    print("[*] Retriving military positions from Navy website...")
    extracted_positions = main_page_scraper.get_career_links()
    if extracted_positions:
        main_page_scraper.save_to_database()
    n = 0 
    for pos in extracted_positions.get("military_positions"):
        print(f"[*] Retriving job details for {pos.get('title')}...")
        scraping_agent = AntScraper(scrap_url=f"https://navy.com{pos.get('details_url')}", extract_type="markdown")
        markdown_content = scraping_agent.get_content().get("markdown")
        position_options = career_translator.get_career_translation(career_page_info=markdown_content)
        if position_options:
            career_translator.save_to_database(military_position_url=pos.get("details_url"))
        n = n + 1
    print(f"[*] We have transalated {n} positions.")


