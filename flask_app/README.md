# Flask Authentication App

A simple Flask web application with user authentication and SQLite database integration.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/flask-auth-app.git
cd flask-auth-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# For sending email
```
Since we are using environment variables for the sake of security. Therefore, setting your email and password as environment variables in your systems
```bash
export MAIL_USERNAME='your-email@example.com'
export MAIL_PASSWORD='your-email-password' 
# Your MAIL_PASSWORD is generated through 2-step factor using app-password on your Google Account
# For example: slgd fjzh erbx iynf

export MAIL_DEFAULT_SENDER='your-default-sender-email@example.com'
```