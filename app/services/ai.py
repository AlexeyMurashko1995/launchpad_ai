from app.core.database import update_startup_ai_response


async def generate_mock_analysis(startup_id: int):
    mock_text = 'string'
    await update_startup_ai_response(startup_id, mock_text)
