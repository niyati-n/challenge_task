from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def gpt_with_prefill(email_text: str, model: str):

    client = openai_client if model == "gpt-5-mini" else openrouter_client

    prompt = f"""
        You are an email extractor.
        Given a raw email text, return a JSON object with the following schema:
        amount
        currency
        due_date
        description
        company
        contact
        Email:
        \"\"\"{email_text}\"\"\"
        """

    completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
                )

    return completion.choices[0].message.content
