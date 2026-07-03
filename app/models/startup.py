from typing import Optional
from sqlmodel import SQLModel, Field

class Startup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str
    total_investment: int | None = None
    ai_response: Optional[str] = None