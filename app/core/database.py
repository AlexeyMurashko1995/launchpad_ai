from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import DATABASE_URL
from app.models.startup import Startup
from sqlmodel import SQLModel, select
from fastapi import BackgroundTasks
from app.services.ai import generate_mock_analysis

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_maker_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_startup(name: str, category: str, background_tasks: BackgroundTasks):
    async with async_maker_factory() as session:
        async with session.begin():
            startup = Startup(name=name, category=category)
            session.add(startup)
        startup_id = startup.id
        background_tasks.add_task(generate_mock_analysis, startup_id)
        return {'status': 'created'}


async def get_all_startups():
    async with async_maker_factory() as session:
        query = select(Startup)
        result = await session.execute(query)
        return result.scalars().all()


async def update_startup_ai_response(startup_id: int, ai_response: str):
    async with async_maker_factory() as session:
        async with session.begin():
            startup = await session.get(Startup, startup_id)
            if startup:
                startup.ai_response = ai_response


async def get_startup_by_id(startup_id: int):
    async with async_maker_factory() as session:
        target_startup = await session.get(Startup, startup_id)
        if target_startup:
            return target_startup