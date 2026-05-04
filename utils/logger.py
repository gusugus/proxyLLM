from loguru import logger
from datetime import datetime
import os
import sys

# logger base (consola)
logger.remove()
logger.add(sys.stdout, level="DEBUG", colorize=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Cache to keep track of active session handlers to avoid duplicates
_session_handlers = {}

def get_session_logger(session_id: str):
    global _session_handlers
    
    # If we already have a handler for this session in THIS process, reuse it
    if session_id in _session_handlers:
        return logger.bind(session=session_id)

    # Otherwise, create a new handler with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{LOG_DIR}/session_{session_id}_{timestamp}.log"
    
    # We use a filter to ensure this handler only gets logs for this specific session
    handler_id = logger.add(
        filename,
        level="DEBUG",
        filter=lambda record: record["extra"].get("session") == session_id,
        rotation="5 MB",
        retention="7 days",
        enqueue=True
    )
    
    _session_handlers[session_id] = handler_id
    return logger.bind(session=session_id)