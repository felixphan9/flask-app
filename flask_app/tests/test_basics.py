import os
import sys

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app
from app.models import User

class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client"""
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_home_page(self):
        """Test that the home page is working"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_404_page(self):
        """Test that the 404 page is working"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Oops! The page you are looking for does not exist.', response.data)
    def test_password_hashing(self):
        """Test that the password hashing is correct"""
        u = User()
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

if __name__ == "__main__":
    unittest.main()