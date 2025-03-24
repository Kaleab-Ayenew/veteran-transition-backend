import json
from app.llm.open_ai import LLMClient
from app.llm import prompts
from app.db import db_utils, models


class ResumeGeneratorAgent:
    def __init__(self):
        self.llm_client = LLMClient(model="gpt-4o-mini",
                                    history=[{"role":"system", "content": prompts.RESUME_GENERATOR_PROMPT}])