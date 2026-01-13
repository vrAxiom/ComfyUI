import json
import os
import requests
from typing import Dict

from prompt_templates import build_prompt

class AIProvider:
    def generate_json(self, subject: str, body: str) -> Dict:
        raise NotImplementedError

class OllamaProvider(AIProvider):
    def __init__(self, base_url: str, model: str):
        self.url = base_url.rstrip("/") + "/api/generate"
        self.model = model

    def generate_json(self, subject: str, body: str) -> Dict:
        prompt = build_prompt(subject, body)
        r = requests.post(self.url, json={"model": self.model, "prompt": prompt, "stream": False}, timeout=20)
        r.raise_for_status()
        payload = r.json()
        text = payload.get("response", "{}")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Basic guardrail: try to extract JSON substring
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                return json.loads(text[start:end+1])
            raise

class LMStudioProvider(AIProvider):
    def __init__(self, base_url: str, model: str, api_key: str | None = None):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.api_key = api_key

    def generate_json(self, subject: str, body: str) -> Dict:
        prompt = build_prompt(subject, body)
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        r = requests.post(
            self.url,
            json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0},
            headers=headers,
            timeout=20,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return json.loads(content)

# Optional cloud providers could be added similarly (OpenAIProvider, GeminiProvider)
