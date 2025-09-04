import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://ai.tigrison.com/gateway/api-legacy/ai/chatgpt/completions"

def ask_gpt(messages, model="gpt-4o"):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "model": model,
        "messages": messages
    }
    r = requests.post(BASE_URL, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")
