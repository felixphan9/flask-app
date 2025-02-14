# Flask Authentication App

A simple Flask web application that implements user authentication with SQLite database integration.

## Installation

Follow these steps to set up the application on your local machine:

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/felixphan9/flask-app.git
cd flask_app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows

# Install required dependencies
pip install -r requirements.txt
```
### Step 2 : Set up the database

The application uses site.db as the default SQLite database. You can create the necessary tables by running the following Python code:

```bash
python
```
```python
from app import db
db.create_all()  # This will create the database tables based on the model
```

### Step 5: Configure Email for Sending Authentication Emails
The app uses environment variables to handle email configuration securely. Set the following environment variables with your email credentials:

```bash
# Set up environment variables for email configuration
export MAIL_USERNAME='your-email@example.com'
export MAIL_PASSWORD='your-email-password'
# Generate your MAIL_PASSWORD using two-step verification and app passwords on Google Account
# Example: 'slgd fjzh erbx iynf'

export MAIL_DEFAULT_SENDER='your-default-sender-email@example.com'
```

Notes:
Ensure you use an app-specific password for `MAIL_PASSWORD` if you're using Google’s 2-step verification.
Replace `your-email@example.com` and `your-default-sender-email@example.com` with your actual email addresses.