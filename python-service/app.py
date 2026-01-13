import os
import time
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_providers import OllamaProvider, LMStudioProvider
from validators import normalize_and_validate
from excel_writer import write_to_excel

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost", "http://localhost:*", "https://*.office.com", "https://*.outlook.com"]}})

AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama").lower()
AI_MODEL = os.getenv("AI_MODEL", "mistral")
EXCEL_PATH = os.getenv("EXCEL_PATH", os.path.expandvars(r"%UserProfile%\\OneDrive\\Documents\\nViteXtracter\\applications.xlsx"))

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if AI_PROVIDER == "ollama":
    provider = OllamaProvider(OLLAMA_URL, AI_MODEL)
elif AI_PROVIDER == "lmstudio":
    provider = LMStudioProvider(LMSTUDIO_BASE_URL, AI_MODEL, api_key=OPENAI_API_KEY)
else:
    # For now, fallback to Ollama
    provider = OllamaProvider(OLLAMA_URL, AI_MODEL)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "provider": AI_PROVIDER, "model": AI_MODEL})

@app.post("/extract")
def extract():
    payload = request.get_json(force=True, silent=True) or {}
    email_body = payload.get("email", "")
    email_subject = payload.get("subject", "")
    from_email = payload.get("from_email")

    try:
        raw = provider.generate_json(email_subject, email_body)
        # inject metadata
        raw["ingested_at"] = datetime.now().isoformat()
        raw["email_subject"] = email_subject
        raw["from_email"] = from_email
        raw["ai_provider"] = AI_PROVIDER
        raw["ai_model"] = AI_MODEL

        data = normalize_and_validate(raw)
        write_to_excel(EXCEL_PATH, data)
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
