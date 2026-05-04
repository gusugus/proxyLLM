import os
from pathlib import Path
from dotenv import load_dotenv

# Asegurar que se carga el archivo .env desde la carpeta del proxy y sobreescribe valores previos
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

LLAMA_AGENT_URL = os.getenv("LLAMA_AGENT_URL")
LLAMACPP_URL = os.getenv("LLAMACPP_URL", "http://localhost:8080")
AUTO_APPROVE = os.getenv("AUTO_APPROVE", "true").lower() == "true"

# Quiz Automation
QUIZ_SAVE_DIR = os.getenv("QUIZ_SAVE_DIR", "./quizzes")
QUIZ_UPLOAD_COMMAND = os.getenv("QUIZ_UPLOAD_COMMAND", "npm start")
QUIZ_UPLOAD_LOG = os.getenv("QUIZ_UPLOAD_LOG", "./logs/uploader.log")

# llama.cpp mode
USE_CHAT_COMPLETIONS = os.getenv("USE_CHAT_COMPLETIONS", "false").lower() == "true"