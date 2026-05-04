import requests
from config import LLAMACPP_URL

def get_completion_response(prompt, options=None):
    """Calls llama.cpp's /completion endpoint (Stateless)."""
    if options is None: options = {}
    payload = {
        "prompt": prompt,
        "stream": True,
        "temperature": options.get("temperature", 1),
        "thinking": True,
    }
    _apply_extra_options(payload, options)
    return requests.post(f"{LLAMACPP_URL}/completion", json=payload, stream=True)

def get_chat_completion_response(messages, options=None):
    """Calls llama.cpp's /v1/chat/completions endpoint (OpenAI style)."""
    if options is None: options = {}
    payload = {
        "messages": messages,
        "stream": True,
        "temperature": options.get("temperature", 1),
    }
    _apply_extra_options(payload, options)
    return requests.post(f"{LLAMACPP_URL}/v1/chat/completions", json=payload, stream=True)

def _apply_extra_options(payload, options):
    if "max_tokens" in options: payload["n_predict"] = options["max_tokens"]
    if "top_p" in options: payload["top_p"] = options["top_p"]
    if "presence_penalty" in options: payload["presence_penalty"] = options["presence_penalty"]
    if "grammar" in options: payload["grammar"] = options["grammar"]
    if "options" in options and isinstance(options["options"], dict):
        payload.update(options["options"])
