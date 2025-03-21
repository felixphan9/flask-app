import unittest
import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, AnonymousUser, Permission

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment and database."""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Push app context and create database tables
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_role(self):
        """Test user permissions based on roles."""
        from app.models import Role  # Import Role inside the test function

        # Ensure a default role exists
        default_role = Role.query.filter_by(default=True).first()
        self.assertIsNotNone(default_role, "Default role does not exist!")

        u = User(email='john@example.com', username='john_doe')  # Add a username
        u.set_password('cat')
        u.role = default_role
        
        db.session.add(u)
        db.session.commit()  # Commit the changes to the database

        # Debugging: Print the user role and permissions
        print(f"User role: {u.role.name}")  # Check the role assigned to the user
        print(f"Role permissions (binary): {bin(u.role.permissions)}")  # Check the permissions bitmask
        
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_anonymous_user(self):
        """Test that anonymous users have no permissions."""
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
        self.assertFalse(u.can(Permission.COMMENT))
        self.assertFalse(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_password_hashing(self):
        """Test password hashing and verification."""
        u = User(email='test@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_home_page(self):
        """Test the home page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_404_page(self):
        """Test handling of non-existent pages."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Oops! The page you are looking for does not exist.', response.data)

if __name__ == "__main__":
    unittest.main()
