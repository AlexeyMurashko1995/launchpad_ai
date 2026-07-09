import asyncio
from app.core.database import init_db, create_startup, get_all_startups
from app.services.ai import generate_mock_analysis
from app.core.database import async_maker_factory


async def main():
    await init_db()
    async with async_maker_factory() as session:
        await create_startup('Test', 'Test_category', session)
    startups = await get_all_startups()
    target_id = startups[0].id
    print(f'Created startup id:{target_id}')
    await generate_mock_analysis(target_id)
    startups = await get_all_startups()
    target_id = startups[0].id
    print(f'Answer:{startups[0].ai_response}')


if __name__ == '__main__':
    asyncio.run(main())