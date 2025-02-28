from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_migrate import Migrate   # Import the Migrate class from the flask_migrate module

mail = Mail() # Create an instance of the Mail class
db = SQLAlchemy() # Create an instance of the SQLAlchemy class
login_manager = LoginManager() # Create an instance of the LoginManager class
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

# This is a factory function that creates a new Flask instance when called. aka app factory
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['development']))  # Default to 'development' if not specified
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)  # Create an instance of the Migrate class
    
    # Blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Authentication Blueprint registration
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
