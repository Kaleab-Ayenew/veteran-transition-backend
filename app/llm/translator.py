import json
from app.llm.open_ai import LLMClient
from app.llm import prompts
from app.db import db_utils, models


class CareerTranslator:
    def __init__(self):
        self.llm_client = LLMClient(model="gpt-4o-mini",
                                    history=[{"role":"system", "content": prompts.JOB_TRANSLATOR_SYSTEM_PROMPT}])
        self.transalted_position = {}
        self.page_markdown = ""
    def get_career_translation(self, career_page_info):
        self.page_markdown = career_page_info
        translated_content = self.llm_client.send_message(input=[{"role":"user", "content": career_page_info}], response_format="json_object")
        translated_positions = json.loads(translated_content)
        self.transalted_position = translated_positions
        return translated_positions
    
    def save_to_database(self, military_position_url: str):
        military_position = db_utils.get_one_row(models.MilitaryPosition, (models.MilitaryPosition.url == military_position_url,))
        if not military_position:
            raise ValueError("The specified military position couldn't be found")
        new_civilian_position = db_utils.create_row(model=models.CivilianPosition, data={
            "extracted_markdown": self.page_markdown,
            "civilian_options": json.dumps(self.transalted_position),
            "military_position": military_position.id
        })
        positions = self.transalted_position.get("civilian_jobs")
        positions = ' \n'.join([a.get("name") for a in positions])
        print(f"[*] Created the following civilian translation for position: {military_position.name}\n {positions}")
