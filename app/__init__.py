from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret'
    app.register_blueprint(bp)
    return app
