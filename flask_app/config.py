import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Define a base configuration class

class Config:
    SECRET_KEY = 'mysecretkey'  # Required for CSRF protection
    # Set the absolute path to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Use environment variables for security
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass  # Add initialization logic for any global app settings here, if needed.

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_PATH = os.path.join('/home/sonphuc/mylittlehobby/flask_app/app/instance', 'site.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'  # Use SQLite with the new path

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use an in-memory database for fast testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# Configuration dictionary to map environment names to configuration classes
config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
# 'production': ProductionConfig,
# 'default': DevelopmentConfig
}