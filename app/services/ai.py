from app.core.config import MISTRAL_API_KEY
import httpx
from pydantic import ValidationError

from app.core.database import (
    async_maker_factory,
    get_startup_by_id,
    update_startup_ai_response,
)
from app.models.startup import StartupAIAnalysis

async def generate_mock_analysis(startup_id: int):
    async with async_maker_factory() as session:
        new_startup = await get_startup_by_id(startup_id, session=session)
        if new_startup:
            ai_text = None
            schema = StartupAIAnalysis.model_json_schema()
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    url = 'https://api.mistral.ai/v1/chat/completions'
                    headers = {'Authorization': f'Bearer {MISTRAL_API_KEY}'}
                    payload = {
                        'model': 'open-mixtral-8x7b',
                        'response_format': {
                            'type': 'json_object',
                            'schema': schema,
                        },
                        'messages': [
                            {
                                'role': 'user',
                                'content': (
                                    f'Analyze: {new_startup.name}, '
                                    f'category: {new_startup.category}'
                                ),
                            }
                        ],
                    }
                    response = await client.post(
                        url, headers=headers, json=payload
                    )
                    data_response = response.json()
                    ai_text = data_response['choices'][0]['message']['content']
                    validated_data = StartupAIAnalysis.model_validate_json(
                        ai_text
                    )
                    ai_text = validated_data.model_dump_json()
            except httpx.HTTPError:
                ai_text = 'Connection error. Please try again later'
            except (KeyError, IndexError):
                ai_text = 'Error processing AI results'
            except ValidationError:
                ai_text = 'Error validating AI results'

            await update_startup_ai_response(startup_id, ai_text)