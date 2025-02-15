import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from config import Config

# Initialize the Flask app
app = Flask(__name__)

# Apply configurations
app.config.from_object(Config)

# Initialize the extensions
mail = Mail(app)
db = SQLAlchemy(app)

# Import parts of our application
from main import routes, models

# Return the app instance for use
def create_app():
    return app
