from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, field_validator
from app.models.user import UserPublic

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


class StartupPublic(BaseModel):
    id: int
    name: str
    category: str
    ai_response: str | None = None
    user: UserPublic | None = None


class StartupUpdate(BaseModel):
    name: str | None = None
    category: str | None = None