import requests
from config import LLAMA_AGENT_URL


def get_chat_response(session_id, message, options=None):
    """Returns the requests.Response object for checking status codes."""
    if options is None:
        options = {}
    
    url = f"{LLAMA_AGENT_URL}/v1/agent/session/{session_id}/chat"
    
    payload = {"content": message}
    payload.update(options)

    return requests.post(
        url,
        json=payload,
        stream=True
    )

def stream_chat(session_id, message, options=None):
    """Original signature preserved but using get_chat_response internally."""
    response = get_chat_response(session_id, message, options)
    for line in response.iter_lines():
        yield line.decode("utf-8")

def create_session():
    r = requests.post(f"{LLAMA_AGENT_URL}/v1/agent/session", json={})
    data = r.json()
    return data["session_id"]