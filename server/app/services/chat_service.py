import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#Intilialize Clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def get_chat_completion(payload: dict):
    model = payload.get("model", "gpt-5-mini")

    client = openai_client if model == "gpt-5-mini" else openrouter_client

    try:
        completion = client.chat.completions.create(
        model=payload["model"],
        messages=payload["messages"],
        max_tokens=payload["max_tokens"]
        )
        return completion
    except Exception as e:
        return {"error": {"message": str(e)}}
