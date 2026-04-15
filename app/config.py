"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-in-production"
    ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "llama3.2")
    MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", 20))
    PORT = os.environ.get("PORT") or "5010"

<<<<<<< HEAD
    LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
    LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING")
    LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT")
=======
    # Configurable chatbot name (env: CHATBOT_NAME)
    CHATBOT_NAME = os.environ.get("CHATBOT_NAME", "Riko")
    # MODEL = os.environ.get("MODEL", "llama3.2")
    AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:5010")


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in Config.ALLOWED_EXTENSIONS
>>>>>>> fdf7e3a2212363ac755e74c61f1bd39f279ff498
