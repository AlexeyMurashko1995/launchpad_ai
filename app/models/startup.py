from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, field_validator
from app.models.user import UserPublic
import json

class Startup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str
    total_investment: int | None = None
    ai_response: Optional[str] = None
    user_id: int | None = Field(foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='startups')


class StartupCreate(BaseModel):
    name: str
    category: str


    @field_validator('name')
    @classmethod
    def clean_name(cls, value: str) -> str:
        return value.strip()


    @field_validator('category')
    @classmethod
    def clean_category(cls, value: str) -> str:
        return value.strip().lower()


class StartupAIAnalysis(BaseModel):
    strengths: list[str] = Field(description='Key advantages of the project')
    weaknesses: list[str] = Field(description='Project weaknesses and vulnerabilities')
    risks: list[str] = Field(description='Potential threats and risks to the business')
    overall_score: int = Field(description='Overall project viability rating (1–10)')


class StartupPublic(BaseModel):
    id: int
    name: str
    category: str
    ai_response: StartupAIAnalysis | None
    user: UserPublic | None = None

    @field_validator('ai_response', mode='before')
    @classmethod
    def parse_ai_response(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return value

class StartupUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
