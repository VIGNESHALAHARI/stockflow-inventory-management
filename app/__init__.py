import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Initialize database and authentication extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    # Create the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Ensure the instance directory exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Load application configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Configure login behavior
    login_manager.login_view = "main.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Prevent browsers from caching private pages
    @app.after_request
    def prevent_private_page_caching(response):
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # Import models and routes after initializing extensions
    from app.models import User, Organization, Product
    from app.routes import main

    # Load authenticated users
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    # Register application routes
    app.register_blueprint(main)

    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()

    return app