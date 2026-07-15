from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import DATABASE_URL
from app.models.startup import Startup, StartupUpdate
from app.models.user import User
from sqlmodel import SQLModel, select

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_maker_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db():
    async with async_maker_factory() as session:
        yield session


async def create_startup(name: str, category: str, user_id: int, session: AsyncSession):
    startup = Startup(name=name, category=category, user_id=user_id)
    session.add(startup)
    await session.commit()
    return startup


async def get_all_startups(session: AsyncSession):
    query = select(Startup).options(joinedload(Startup.user))
    result = await session.execute(query)
    return result.scalars().all()


async def update_startup_ai_response(startup_id: int, ai_response: str):
    async with async_maker_factory() as session:
        async with session.begin():
            startup = await session.get(Startup, startup_id)
            if startup:
                startup.ai_response = ai_response


async def get_startup_by_id(startup_id: int, session: AsyncSession):
    query = select(Startup).where(startup_id==Startup.id).options(joinedload(Startup.user))
    result = await session.execute(query)
    target_startup = result.scalar_one_or_none()
    if target_startup:
        return target_startup


async def delete_startup(startup_id: int, session: AsyncSession):
    async with session.begin():
        target_startup = await session.get(Startup, startup_id)
        if not target_startup:
            return False
        session.delete(target_startup)
        return True


async def update_startup(startup_id: int, startup_data: StartupUpdate, session: AsyncSession):
    async with session.begin():
        startup = await session.get(Startup, startup_id)
        if not startup:
            return None
        update_dict = startup_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(startup, key, value)
        return startup