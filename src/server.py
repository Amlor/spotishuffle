from flask import Flask
from src.test_handlers import mod as test

def create_app():
    app = Flask(__name__)
    configure_blueprints(app)
    return app


def configure_blueprints(app):
    app.register_blueprint(test, url_prefix='/test')
    app.register_blueprint(api, url_prefix='/api/v1')
