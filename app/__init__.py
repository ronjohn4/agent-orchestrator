"""Flask application factory."""
from flask import Flask
from flask_restful import Api
from app.config import Config

flask_api = Api()

def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

<<<<<<< HEAD
    from app.api import bp as api_bp
    flask_api.init_app(api_bp)
    app.register_blueprint(api_bp)
=======
    # Ensure upload directory exists
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    @app.context_processor
    def inject_chatbot_name():
        return {"chatbot_name": app.config["CHATBOT_NAME"]}

    HTMX(app)

    from app.routes import chat
    app.register_blueprint(chat.bp)
>>>>>>> fdf7e3a2212363ac755e74c61f1bd39f279ff498

    return app
