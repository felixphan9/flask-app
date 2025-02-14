import os

class Config:
    SECRET_KEY = 'mysecretkey'  # Required for CSRF protection
    # Set the absolute path to the database
    DATABASE_PATH = os.path.join('/home/sonphuc/mylittlehobby/flask_app/app/instance', 'site.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'  # Use SQLite with the new path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Use environment variables for security
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    DEBUG = True
