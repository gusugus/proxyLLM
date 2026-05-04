from flask import Blueprint, request, Response
from services.rules import apply_rules
from services.chat_orchestrator import get_backend_response
from services.stream_handler import get_stream_generator
from utils.logger import get_session_logger
# Historial manejado por cliente

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat/<session_id>", methods=["POST"])
def chat(session_id):
    logger = get_session_logger(session_id)
    data = request.json
    backend = data.get("backend", "llamacpp")
    options = _parse_options(data)

    user_msg = data.get("message", "")
    logger.info(f"[CHAT] backend={backend} | msg={user_msg}")
    
    # Session History (now coming from client)
    history = data.get("history", [])
    if history:
        logger.info(f"[CHAT] {len(history)} history messages received from client")

    preguntas = data.get("preguntas", [])
    for q in preguntas:
        if "playerAnswer" in q:
            q["studentAnswer"] = q.pop("playerAnswer")
            
    if preguntas:
        logger.info(f"[CHAT] {len(preguntas)} failed questions received")
    
    materia = data.get("materia", "")
    options["preguntas"] = preguntas
    options["materia"] = materia

    final_msg = apply_rules(user_msg, backend=backend, preguntas=preguntas, materia=materia, history=history)

    if preguntas or materia or history:
        logger.info(f"[TUTOR] Full prompt sent to LLM:\n{final_msg}")

    agent_res = get_backend_response(session_id, final_msg, backend, options)

    if not agent_res.ok:
        return {"error": "Backend error", "status": agent_res.status_code}, agent_res.status_code

    generator = get_stream_generator(agent_res, backend, options, session_id=session_id)
    return Response(generator(), mimetype="text/event-stream")

def _parse_options(data):
    options = {
        "temperature": data.get("temperature"),
        "max_tokens": data.get("max_tokens"),
        "top_p": data.get("top_p"),
        "presence_penalty": data.get("presence_penalty"),
        "thinking": data.get("thinking", True),
        "preguntas": data.get("preguntas", []),
        "materia": data.get("materia", ""),
    }
    if "options" in data and isinstance(data["options"], dict):
        extra = data["options"].copy()
        extra.update({k: v for k, v in options.items() if v is not None})
        options = extra
    return {k: v for k, v in options.items() if v is not None}