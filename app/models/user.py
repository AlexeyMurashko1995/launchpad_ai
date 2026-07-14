from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    startups: list['Startup'] = Relationship(back_populates='user')


class UserCreate(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str