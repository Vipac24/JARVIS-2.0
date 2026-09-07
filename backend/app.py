from flask import Flask, request, jsonify, send_from_directory
import os
import sys
import requests
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from memory.store import save_memory, search_memory
from tools.web_search import web_search
from tools.system_tools import get_time, get_date, battery, flashlight, volume_up, volume_down, mute, vibrate, device_info, wifi_status, notify, camera_photo

app = Flask(__name__)

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
AI_URL = "http://127.0.0.1:8080/v1/chat/completions"

SYSTEM_PROMPT = """
You are JARVIS 2.0, a highly capable personal AI assistant.
Address the user respectfully as Sir when appropriate.
Be intelligent, concise, helpful and natural.
Understand English, Hindi and Hinglish.
Never claim an action was performed unless it actually was.
"""

def ask_ai(message, extra_context=""):
    brain_url = os.environ.get("JARVIS_BRAIN_URL", "").rstrip("/")
    brain_key = os.environ.get("JARVIS_BRAIN_KEY", "")

    if brain_url and brain_key:
        try:
            r = requests.post(
                brain_url + "/chat",
                headers={"X-JARVIS-Key": brain_key},
                json={"message": message},
                timeout=60
            )
            r.raise_for_status()
            return r.json().get("reply", "Sir, brain returned no reply.")
        except Exception as e:
            return f"Sir, my mobile brain is temporarily unavailable: {e}"

    response = requests.post(
        AI_URL,
        json={
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT + extra_context
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.5,
            "max_tokens": 64,
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
        timeout=30
    )

    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def detect_tool(message):
    text = message.lower()

    time_words = [
        "time kya hai", "what time", "current time",
        "kitne baje", "samay kya hai", "time batao"
    ]

    date_words = [
        "date kya hai", "what date", "today's date",
        "aaj ki date", "aaj kya date", "date batao"
    ]

    flashlight_on_words = [
        "flashlight on", "torch on", "flash on",
        "light on", "flashlight chalao", "torch chalao"
    ]

    flashlight_off_words = [
        "flashlight off", "torch off", "flash off",
        "light off", "flashlight band", "torch band"
    ]

    volume_up_words = ["volume up", "volume badhao", "awaz badhao", "sound badhao"]
    volume_down_words = ["volume down", "volume kam", "awaz kam", "sound kam"]
    mute_words = ["mute", "awaz band", "sound band"]
    vibrate_words = ["vibrate", "phone vibrate", "vibration"]
    wifi_words = ["wifi status", "wifi connected", "wifi check"]
    device_words = ["device info", "phone info", "mobile info"]
    notify_words = ["notification bhejo", "notify me"]

    camera_words = [
        "camera", "photo lo", "photo lena", "picture lo",
        "pic lo", "camera chalao", "camera se dekho"
    ]

    battery_words = [
        "battery", "charge kitna", "battery kitni",
        "charge kitna hai", "battery status"
    ]

    if any(word in text for word in time_words):
        return "time"

    if any(word in text for word in date_words):
        return "date"

    if any(word in text for word in flashlight_on_words):
        return "flashlight_on"

    if any(word in text for word in flashlight_off_words):
        return "flashlight_off"

    if any(word in text for word in volume_up_words):
        return "volume_up"

    if any(word in text for word in volume_down_words):
        return "volume_down"

    if any(word in text for word in mute_words):
        return "mute"

    if any(word in text for word in vibrate_words):
        return "vibrate"

    if any(word in text for word in wifi_words):
        return "wifi_status"

    if any(word in text for word in device_words):
        return "device_info"

    if any(word in text for word in notify_words):
        return "notify"

    if any(word in text for word in battery_words):
        return "battery"

    return None

def needs_web_search(message):
    keywords = [
        "search", "google", "latest", "today", "news",
        "current", "live", "recent", "abhi", "aaj",
        "internet", "web"
    ]
    text = message.lower()
    return any(k in text for k in keywords)

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "status": "online",
        "ai_brain": "Qwen3-0.6B Q8_0",
        "memory": "online",
        "web_search": "online",
        "tools": "online",
        "engine": "llama.cpp"
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "reply": "Yes Sir. I'm listening.",
            "status": "success"
        })

    try:
        # Real device tools
        tool = detect_tool(message)

        if tool == "time":
            reply = f"Sir, the current time is {get_time()}."
            return jsonify({"reply": reply, "status": "success"})

        if tool == "date":
            reply = f"Sir, today's date is {get_date()}."
            return jsonify({"reply": reply, "status": "success"})

        if tool == "flashlight_on":
            reply = flashlight("on")
            return jsonify({"reply": f"Sir, {reply}", "status": "success"})

        if tool == "flashlight_off":
            reply = flashlight("off")
            return jsonify({"reply": f"Sir, {reply}", "status": "success"})

        if tool == "volume_up":
            return jsonify({"reply": f"Sir, {volume_up()}", "status": "success"})

        if tool == "volume_down":
            return jsonify({"reply": f"Sir, {volume_down()}", "status": "success"})

        if tool == "mute":
            return jsonify({"reply": f"Sir, {mute()}", "status": "success"})

        if tool == "vibrate":
            return jsonify({"reply": f"Sir, {vibrate()}", "status": "success"})

        if tool == "wifi_status":
            return jsonify({"reply": f"Sir, Wi-Fi information: {wifi_status()}", "status": "success"})

        if tool == "device_info":
            return jsonify({"reply": f"Sir, device information: {device_info()}", "status": "success"})

        if tool == "notify":
            return jsonify({"reply": f"Sir, {notify('JARVIS', 'JARVIS notification test')}", "status": "success"})

        if tool == "camera":
            result = camera_photo(0)
            return jsonify({"reply": f"Sir, {result}", "status": "success", "image": "/vision/latest.jpg"})

        if tool == "battery":
            raw = battery()
            try:
                info = json.loads(raw)
                percent = info.get("percentage")
                status_text = info.get("status", "")
                reply = f"Sir, your battery is at {percent}%"
                if status_text:
                    reply += f" and the status is {status_text.lower()}."
                else:
                    reply += "."
            except:
                reply = f"Sir, battery information: {raw}"
            return jsonify({"reply": reply, "status": "success"})

        # Memory + web context for AI
        context = ""

        memories = search_memory(message)
        if memories:
            context += "\nRelevant memory:\n"
            context += "\n".join(
                "- " + item["text"] for item in memories
            )

        if needs_web_search(message):
            results = web_search(message, 3)
            if results and not results[0].get("error"):
                context += "\n\nLIVE WEB SEARCH RESULTS:\n"
                for i, result in enumerate(results, 1):
                    context += (
                        f"\n{i}. {result['title']}\n"
                        f"URL: {result['url']}\n"
                        f"Info: {result['snippet']}\n"
                    )

        reply = ask_ai(message, context)

        if len(message) >= 8:
            save_memory(message)

        return jsonify({
            "reply": reply,
            "status": "success"
        })

    except Exception as e:
        print("JARVIS ERROR:", e)
        return jsonify({
            "reply": "Sir, something went wrong while processing that request.",
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
