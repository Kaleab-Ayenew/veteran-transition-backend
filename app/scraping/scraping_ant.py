import http.client
from urllib.parse import quote
from typing import Literal
import json
from app.config import settings


class AntScraper:
    def __init__(self, scrap_url: str, extract_type: Literal['markdown', 'extended', 'general'] = "markdown"):
        self.http_connection = http.client.HTTPSConnection("api.scrapingant.com")
        self.request_url = f"/v2/{extract_type}?url={quote(scrap_url, safe=':/?=&')}&x-api-key={settings.ANT_SCRAPER_KEY}&proxy_country=US"
        self.extract_type = extract_type
        self.scrap_url = scrap_url
    def get_content(self):
        print(f"[*] Scraping content from {self.scrap_url}")
        self.http_connection.request("GET", self.request_url)
        res = self.http_connection.getresponse()
        data = res.read().decode("utf-8")
        if self.extract_type == "markdown":
            final_response = json.loads(data)
            final_response = final_response.get("markdown")
            return final_response
        elif self.extract_type == "extended":
            final_response = json.loads(data)
            return final_response
        return data
    
if __name__ == "__main__":
    ant = AntScraper(scrap_url="https://www.navy.com/careers-benefits/careers",
                     extract_type="markdown")
    content = ant.get_content()
    print(content)