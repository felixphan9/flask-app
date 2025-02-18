from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemys

# Import the Config class
from config import Config

mail = Mail()
db = SQLAlchemy()
