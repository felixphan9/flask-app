from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app

class Permission:
    """Permissions for user roles"""
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    """Role model for user roles (e.g., Admin, User, Moderator)"""
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Role name (e.g., Admin, User)
    default = db.Column(db.Boolean, default=False, index=True) # Default role for new users
    permissions = db.Column(db.Integer, default=0) # Permissions for the role    
    users = db.relationship('User', back_populates='role')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def has_permission(self, perm):
        """Check if role has a specific permission."""
        return (self.permissions & perm) == perm

    def add_permission(self, perm):
        """Add a permission to the role."""
        if not self.has_permission(perm):
            self.permissions |= perm

    def remove_permission(self, perm):
        """Remove a permission from the role."""
        if self.has_permission(perm):
            self.permissions &= ~perm

    def reset_permissions(self):
        """Reset all permissions to zero."""
        self.permissions = 0
    
    @staticmethod
    def insert_roles():
        """Initialize roles in the database."""
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Admin': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
        }

        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) # Username is unique
    email = db.Column(db.String(120), unique=True, nullable=False) # Email is unique
    password_hash = db.Column(db.String(120), nullable=False) # Hashed password
    confirmed = db.Column(db.Boolean, default=False)  # Indicates if the email has been confirmed
    confirmed_on = db.Column(db.DateTime, nullable=True)  # Optional: When the confirmation occurred
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Role ID (Foreign Key)
    role = db.relationship('Role', back_populates='users')  # Relationship with Role model
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            # Assign the "Administrator" role if the user's email matches the admin email in config
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            # If no role is found, assign the default role
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

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
    
    def has_permission(self, perm):
        """Check if user has a specific permission through their role."""
        return self.role is not None and self.role.has_permission(perm)
    
    def can(self, perm):
        """Check if the user has a certain permission (overriding UserMixin's method)."""
        return self.has_permission(perm)

    def is_administrator(self):
        """Check if the user is an administrator."""
        return self.can(Permission.ADMIN)
    
# Anonymous User Class
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

# Set up anonymous user
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))