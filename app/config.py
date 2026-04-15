"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-in-production"
    UPLOAD_FOLDER = Path(os.environ.get("UPLOAD_FOLDER", "uploads")).resolve()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

    # Configurable chatbot name (env: CHATBOT_NAME)
    CHATBOT_NAME = os.environ.get("CHATBOT_NAME", "Riko")
    # MODEL = os.environ.get("MODEL", "llama3.2")
    AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:5010")


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in Config.ALLOWED_EXTENSIONS
