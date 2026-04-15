"""Flask application factory."""
from pathlib import Path

from flask import Flask
from flask_htmx import HTMX

from app.config import Config


def create_app(config_object=Config) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_object)

    # Ensure upload directory exists
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    @app.context_processor
    def inject_chatbot_name():
        return {"chatbot_name": app.config["CHATBOT_NAME"]}

    HTMX(app)

    from app.routes import chat
    app.register_blueprint(chat.bp)

    return app
