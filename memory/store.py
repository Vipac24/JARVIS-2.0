import json
import os
from datetime import datetime

MEMORY_FILE = os.path.expanduser("~/JARVIS-2.0/memory/memory.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_memory(text):
    memories = load_memory()
    memories.append({
        "text": text,
        "time": datetime.now().isoformat()
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=2)

def search_memory(query):
    memories = load_memory()
    words = query.lower().split()

    results = []
    for item in memories:
        text = item["text"].lower()
        if any(word in text for word in words):
            results.append(item)

    return results[-5:]
