from sqlmodel import SQLModel, Field, TEXT, JSON
import uuid
import datetime
import json


def get_uuid_string():
    return str(uuid.uuid4())
def get_utc_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)

class MilitaryPosition(SQLModel, table=True):
    __tablename__ = "military_position"
    id: str = Field(default_factory=get_uuid_string, primary_key=True)
    name: str = Field(nullable=True)
    url: str = Field(nullable=True)
    category: str = Field(nullable=True)
    created_at: datetime.datetime = Field(default_factory=get_utc_now)

class CivilianPosition(SQLModel, table=True):
    __tablename__ = "civilian_position"
    id: str = Field(default_factory=get_uuid_string, primary_key=True)
    extracted_markdown: str = Field(sa_column=TEXT)
    civilian_options: str = Field(sa_column=TEXT)
    created_at: datetime.datetime = Field(default_factory=get_utc_now)

    military_position: str = Field(foreign_key="military_position.id")

    def get_civilian_options(self):
        """
        ```json
        {
        "civilian_jobs": [
            {
            "name": "<the-name-of-the-matching-position>",
            "description": "<description of the matching position>",
            "match_rank": 0
            },
            {
            "name": "<the-name-of-the-next-matching-position>",
            "description": "<description of the next matching position>",
            "match_rank": 1
            },
            {
            "name": "<the-name-of-the-least-matching-position>",
            "description": "<description of the least matching position>",
            "match_rank": 2
            }
        ]
        }
        ```"""
        return json.loads(self.civilian_options)