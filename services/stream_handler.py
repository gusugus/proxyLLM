import json
from loguru import logger
from services.persistence_service import save_response_to_json
from services.automation_service import run_automation_command

def get_stream_generator(agent_res, backend, options, session_id=None):
    """Generator that harmonizes SSE streams from different backends."""
    def generate():
        accumulated_content = ""
        accumulated_thought = ""
        is_quiz = "grammar" in options
        s_logger = logger.bind(session=session_id) if session_id else logger

        for line in agent_res.iter_lines():
            raw_line = line.decode("utf-8")
            if not raw_line.strip() and backend != "llamacpp":
                yield raw_line + "\n"
                continue

            if backend == "llamacpp":
                result = _handle_llamacpp_line(raw_line)
                if result:
                    content, thought, stats, stop = result
                    if thought:
                        accumulated_thought += thought
                        s_logger.debug(f"[LLM THOUGHT] {thought}")
                    if content:
                        accumulated_content += content
                        s_logger.debug(f"[LLM CHUNK] {content}")
                    yield f"event: text_delta\ndata: {json.dumps({'content': content, 'thought': thought})}\n\n"
                    if stop:
                        if accumulated_thought: s_logger.info(f"[LLM] Complete thought:\n{accumulated_thought}")
                        s_logger.info(f"[LLM] Complete response:\n{accumulated_content}")
                        # El historial ahora se maneja en el cliente
                        yield f"event: completed\ndata: {json.dumps({'reason': 'stop', 'stats': stats})}\n\n"
                        _trigger_post_generation(is_quiz, accumulated_content)
                        break
            else:
                if raw_line.startswith("data:"):
                    try:
                        data = json.loads(raw_line[5:].strip())
                        if "content" in data:
                            chunk = data["content"]
                            accumulated_content += chunk
                            s_logger.debug(f"[LLM CHUNK] {chunk}")
                        if data.get("reason") == "completed" or data.get("stop"):
                             s_logger.info(f"[LLM] Complete response:\n{accumulated_content}")
                             # El historial ahora se maneja en el cliente
                    except: pass
                yield raw_line + "\n"
    return generate

def _handle_llamacpp_line(raw_line):
    if not raw_line.startswith("data:"): return None
    try:
        data = json.loads(raw_line.replace("data:", "").strip())
        return data.get("content", ""), data.get("thought", ""), {
                "input_tokens": data.get("tokens_evaluated", 0),
                "output_tokens": data.get("tokens_predicted", 0)
            }, data.get("stop", False)
    except: return None

def _trigger_post_generation(is_quiz, content):
    if is_quiz and content:
        save_response_to_json(content)
        run_automation_command()
