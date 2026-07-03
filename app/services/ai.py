from app.core.database import update_startup_ai_response, get_startup_by_id
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('MISTRAL_API_KEY')

async def generate_mock_analysis(startup_id: int):
    new_startup = await get_startup_by_id(startup_id)
    if new_startup:
        async with httpx.AsyncClient(timeout=30.0) as client:
            url = 'https://api.mistral.ai/v1/chat/completions'
            headers = {'Authorization': f'Bearer {API_KEY}'}
            payload = {'model': 'open-mixtral-8x7b', 'messages': [{'role': 'user', 'content': f'Analyze: {new_startup.name}, category: {new_startup.category}'}]}
            response = await client.post(url, headers=headers, json=payload)
            print(response.status_code)
            mock_text = f'Startup name: {new_startup.name}; category: {new_startup.category}'
            await update_startup_ai_response(startup_id, mock_text)
