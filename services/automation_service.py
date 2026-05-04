import os
import time
import subprocess
import threading
import atexit
from loguru import logger
from config import QUIZ_UPLOAD_COMMAND, QUIZ_UPLOAD_LOG

_active_process = None
_lock = threading.Lock()

def run_automation_command():
    """Triggers the background automation command if not already running."""
    global _active_process
    def run():
        global _active_process
        with _lock:
            if _active_process is None or _active_process.poll() is not None:
                _start_automation_node()
            else:
                logger.debug(f"[AUTOMATION] Already active (PID: {_active_process.pid})")
    threading.Thread(target=run, daemon=True).start()

def _start_automation_node():
    global _active_process
    try:
        log_path = os.path.abspath(QUIZ_UPLOAD_LOG)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- {time.ctime()}: STARTING AUTOMATION ---\n")
            _active_process = subprocess.Popen(
                QUIZ_UPLOAD_COMMAND, shell=True, stdout=f, stderr=f, text=True
            )
            logger.info(f"[AUTOMATION] Started process (PID: {_active_process.pid})")
    except Exception as e:
        logger.error(f"[AUTOMATION] Execution failed: {e}")

@atexit.register
def _shutdown_automation():
    global _active_process
    if _active_process and _active_process.poll() is None:
        logger.info(f"[AUTOMATION] Shutting down PID: {_active_process.pid}...")
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(_active_process.pid)], capture_output=True)
        else:
            _active_process.terminate()
