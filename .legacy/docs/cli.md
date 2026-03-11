setx OPENAI_API_KEY "your_api_key_here"

## Com .venv ativado:

uvicorn monagent.api.app:app --reload --port 8000
