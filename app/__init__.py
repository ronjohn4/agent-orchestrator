"""Flask application factory."""
from flask import Flask
from flask_restful import Api
from app.config import Config

flask_api = Api()

def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    from app.api import bp as api_bp
    flask_api.init_app(api_bp)
    app.register_blueprint(api_bp)

    return app
