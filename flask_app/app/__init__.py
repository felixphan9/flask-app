from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

mail = Mail()
db = SQLAlchemy()
# This is a factory function that creates a new Flask instance when called. aka app factory
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['development']))  # Default to 'development' if not specified
    mail.init_app(app)
    db.init_app(app)

    # Blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
