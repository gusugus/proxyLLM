import requests
from flask import request
import json
from config import LLAMA_AGENT_URL
from flask import Flask


def should_auto_approve(tool: str, details: dict) -> bool:
    if tool == "write":
        path = details.get("file_path", "")
        return path.startswith("/tmp")

    if tool == "bash":
        # puedes ajustar esto
        return True

    return True


def send_permission(request_id, allow):
    r = requests.post(
        f"{LLAMA_AGENT_URL}/v1/agent/permission/{request_id}",
        json={
            "allow": allow,
            "scope": "once"
        }
    )

    return r.ok