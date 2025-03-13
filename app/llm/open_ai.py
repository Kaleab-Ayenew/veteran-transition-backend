from openai import OpenAI
from typing import Literal
from app.config import settings


class LLMClient:
    def __init__(self, model: Literal['gpt-4o', 'gpt-4o-mini'] = "gpt-4o-mini", history: list = []):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.history = history
        self.model = model

    def send_message(self, input: list, response_format: Literal['text', 'json_object', 'json_schema'] = 'text'):
        self.history.extend(input)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            response_format= {
                "type": response_format
                },
            temperature=0.1
        )
        rsp_content = response.choices[0].message.content
        new_history = [{"role": "assistant", "content": rsp_content}]
        self.history.extend(new_history)
        return response.choices[0].message.content

