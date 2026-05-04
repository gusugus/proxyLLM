import os
from loguru import logger
from services.llama_agent import create_session, get_chat_response
from services.llamacpp_service import get_completion_response, get_chat_completion_response
from services.grammar_service import apply_quiz_grammar
from config import USE_CHAT_COMPLETIONS

def get_backend_response(session_id, message, backend, options):
    """Orchestrates the call to the appropriate LLM backend."""
    if backend == "llamacpp":
        return _handle_llamacpp(message, options)
    return _handle_llama_agents(session_id, message, options)

def _handle_llamacpp(message, options):
    logger.info(f"[ORCHESTRATOR] Routing to llama.cpp (ChatMode={USE_CHAT_COMPLETIONS})")
    
    # Extract original user message for intent detection
    parts = message.split("\n\nUsuario:\n")
    user_message = parts[-1] if len(parts) > 1 else message

    if not options.get("preguntas"):
        msg_lower = user_message.lower()
        if any(kw in msg_lower for kw in ["pregunta", "opciones", "quiz", "cuestionario"]):
            apply_quiz_grammar(options)
        
    if USE_CHAT_COMPLETIONS:
        messages = [{"role": "user", "content": message}]
        return get_chat_completion_response(messages, options=options)
        
    return get_completion_response(message, options=options)

def _handle_llama_agents(session_id, message, options):
    logger.info("[ORCHESTRATOR] Routing to llama-agents")
    if session_id == "new": session_id = create_session()
    return get_chat_response(session_id, message, options=options)
