from app.core.database import update_startup_ai_response, get_startup_by_id, async_maker_factory
from app.models.startup import StartupAIAnalysis
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('MISTRAL_API_KEY')

async def generate_mock_analysis(startup_id: int):
    async with async_maker_factory() as session:
        new_startup = await get_startup_by_id(startup_id, session=session)
        if new_startup:
            ai_text = None
            schema = StartupAIAnalysis.model_json_schema()
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    url = 'https://api.mistral.ai/v1/chat/completions'
                    headers = {'Authorization': f'Bearer {API_KEY}'}
                    payload = {'model': 'open-mixtral-8x7b', 'response_format': {'type': 'json_object', 'schema': schema}, 'messages': [{'role': 'user', 'content': f'Analyze: {new_startup.name}, category: {new_startup.category}'}]}
                    response = await client.post(url, headers=headers, json=payload)
                    data_response = response.json()
                    ai_text = data_response['choices'][0]['message']['content']
            except httpx.HTTPError as net_err:
                ai_text = 'Connection error. Please try again later'
            except (KeyError, IndexError) as parse_err:
                ai_text = 'Error processing AI results'
            await update_startup_ai_response(startup_id, ai_text)