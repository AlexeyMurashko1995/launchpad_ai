from app.core.database import update_startup_ai_response, get_startup_by_id
import httpx


async def generate_mock_analysis(startup_id: int):
    new_startup = await get_startup_by_id(startup_id)
    if new_startup:
        async with httpx.AsyncClient() as client:
            url = 'https://api.mistral.ai/v1/chat/completions'
            headers = {'Authorization': f'Bearer My_Key'}
            payload = {'model': 'open-mixtral-8x7b'}
            response = await client.post(url, headers=headers, json=payload)
            print(response.status_code)
            mock_text = f'Startup name: {new_startup.name}; category: {new_startup.category}'
            await update_startup_ai_response(startup_id, mock_text)
