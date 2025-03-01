import requests
import json
import os
from dotenv import load_dotenv


def ask_openrouter(question: str) -> str:
    load_dotenv()
    API_TOKEN = os.getenv('API_KEY')

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                    ]
                }
            ],
        })
    )

    response_json = response.json()
    return response_json["choices"][0]["message"]["content"].strip()


print(ask_openrouter("What is the capital of France?"))
