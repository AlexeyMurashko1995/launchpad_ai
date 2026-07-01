from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import DATABASE_URL
from app.models.startup import Startup
from sqlmodel import SQLModel

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_maker_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)