"""Application configuration."""
import os
from pathlib import Path


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-in-production"
    ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "llama3.2")
    MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", 20))
    PORT = os.environ.get("PORT") or "5010"

    LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
    LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING")
    LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT")
