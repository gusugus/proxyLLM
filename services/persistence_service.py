import os
import json
import time
from loguru import logger
from config import QUIZ_SAVE_DIR

_chat_history = {}

def save_response_to_json(content):
    """Saves a text response (expecting JSON) to a file."""
    try:
        clean_text = _extract_json(content)
        data = json.loads(clean_text)
        save_dir = os.path.abspath(QUIZ_SAVE_DIR)
        os.makedirs(save_dir, exist_ok=True)
        filepath = _generate_filepath(save_dir, data)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return filepath
    except Exception as e:
        logger.error(f"[PERSISTENCE] Save error: {e}")
        return None

def get_history(session_id, limit=6):
    """Returns the last messages of the session for memory support."""
    return _chat_history.get(session_id, [])[-limit:]

def add_to_history(session_id, role, content):
    """Adds a message to the session history."""
    if session_id not in _chat_history:
        _chat_history[session_id] = []
    _chat_history[session_id].append({"role": role, "content": content})

def _extract_json(text):
    text = text.strip()
    if "{" in text and "}" in text:
        return text[text.find("{"):text.rfind("}") + 1]
    return text

def _generate_filepath(directory, data):
    subject = data.get("subject", "response").replace(" ", "_").lower()
    subject = "".join(c for c in subject if c.isalnum() or c == "_")
    return os.path.join(directory, f"data_{subject}_{int(time.time())}.json")
