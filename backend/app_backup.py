from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

AI_URL = "http://127.0.0.1:8080/v1/chat/completions"

SYSTEM_PROMPT = """
You are JARVIS 2.0, a highly capable personal AI assistant.
Address the user respectfully as Sir when appropriate.
Be intelligent, concise, helpful and natural.
You understand English, Hindi and Hinglish.
Never claim that you performed an action unless it was actually performed.
Currently you are the conversation brain. Device controls and other tools will be connected later.
"""

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "ai_brain": "Qwen3-1.7B",
        "engine": "llama.cpp"
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"reply": "Yes Sir. I'm listening.", "status": "success"})

    try:
        response = requests.post(
            AI_URL,
            json={
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.7,
                "max_tokens": 256,
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            },
            timeout=120
        )

        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"].strip()

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        print("AI ERROR:", e)
        return jsonify({
            "reply": "Sir, I cannot reach my AI brain right now.",
            "status": "error"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
