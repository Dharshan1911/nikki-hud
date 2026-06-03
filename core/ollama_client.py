import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_nikki(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:14b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    return response.json()["response"]


def stream_nikki(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "qwen3:14b",
            "prompt": prompt,
            "stream": True,
            "think": False,
        },
        stream=True,
        timeout=300,
    )

    for line in response.iter_lines():

        if not line:
            continue

        data = json.loads(line)

        if "response" in data:
            yield data["response"]

        if data.get("done", False):
            break
