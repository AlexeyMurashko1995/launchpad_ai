from app.core.database import update_startup_ai_response, get_startup_by_id


async def generate_mock_analysis(startup_id: int):
    new_startup = await get_startup_by_id(startup_id)
    if new_startup:
        mock_text = f'Startup name: {new_startup.name}; category: {new_startup.category}'
        await update_startup_ai_response(startup_id, mock_text)
