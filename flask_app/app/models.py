from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_login import UserMixin
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Username is unique
    email = db.Column(db.String(120), unique=True, nullable=False) # Email is unique
    password_hash = db.Column(db.String(120), nullable=False) # Hashed password
    confirmed = db.Column(db.Boolean, default=False)  # Indicates if the email has been confirmed
    confirmed_on = db.Column(db.DateTime, nullable=True)  # Optional: When the confirmation occurred

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_token(self, expires_in=3600):
        """
        Generate a cryptographic token that contains the user name.
        The token will expire in `expires_in` seconds.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        # Note: In newer versions of itsdangerous, dumps returns a string directly.
        token = s.dumps({'username': self.username}, salt='email-confirm')
        print('token:', token)
        return token
    
    @staticmethod
    def verify_token(token, expires_in=3600):
        """
        Verify the token and return the corresponding user if the token is valid,
        otherwise return None.
        """
        s = Serializer(current_app.config['SECRET_KEY'])

        # Note: In newer versions of itsdangerous, loads returns a string directly.
        try:
            data = s.loads(token, salt='email-confirm', max_age=expires_in)
            print('Decoded token data:', data)  # Debug: Show decoded token data
        except SignatureExpired:
            print("Token has expired.")
            return None
        except BadSignature:
            print("Token is invalid (bad signature).")
            return None  # Invalid token

        username = data.get('username')
        if username:
            return User.query.filter_by(username=username).first()
        return None
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))