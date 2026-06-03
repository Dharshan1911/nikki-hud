import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_nikki(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:14b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    return response.json()["response"]
