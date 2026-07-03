import asyncio
from app.core.database import init_db, create_startup, get_all_startups
from app.services.ai import generate_mock_analysis


async def main():
    await init_db()
    await create_startup('Test', 'Test_category')
    startups = await get_all_startups()
    target_id = startups[0].id
    print(f'Created startup id:{target_id}')
    await generate_mock_analysis(target_id)
    startups = await get_all_startups()
    target_id = startups[0].id
    print(f'Answer:{startups[0].ai_response}')


if __name__ == '__main__':
    asyncio.run(main())