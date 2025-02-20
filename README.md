# Flask Authentication App

A simple Flask web application that implements user authentication with SQLite database integration.

# Project Structure
flasky/
├── app/
│   ├── instance/
│   │   └── site.db            # SQLite database file
│   ├── templates/
│   │   ├── 404.html           # Custom 404 error page
│   │   ├── email.html         # Email sending page
│   │   ├── index.html         # Home page
│   │   ├── login.html         # Login page
│   │   └── register.html      # Registration page
│   ├── static/                # Static assets (CSS, JavaScript, images)
│   ├── main/
│   │   ├── __init__.py        # Initializes the main module (blueprint)
│   │   ├── client.py          # Client-related functionalities (API calls, etc.)
│   │   ├── errors.py          # Error handlers for the main module
│   │   ├── forms.py           # Form definitions
│   │   └── views.py           # View functions for the main module
│   ├── app.py                 # Main app file (creates the Flask instance)
│   ├── __init__.py            # Application factory and initialization
│   ├── email.py               # Email handling logic
│   └── models.py              # Database models
├── migrations/                # Database migration scripts
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test*.py               # Test cases
├── requirements.txt           # Project dependencies
├── youdontexist               # Unspecified file (check if needed)
├── config.py                  # Application configuration settings
└── flasky.py                  # Application entry point


## Installation

Follow these steps to set up the application on your local machine:

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/felixphan9/flask-app.git
cd flask_app
```

### Step 2 Activate a Virtual Environment
```bash
# Activate the virtual environment
source youdontexist/bin/activate  # On Linux/Mac
# or
.\youdontexist\Scripts\activate  # On Windows
```

### Step 3 Install Dependencies
```bash
# Install required dependencies
pip install -r requirements.txt
```

### Step 4: Configure Email for Sending Authentication Emails
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

### Step 5. Specify the Application Entry Point

efore running the app, ensure that Flask uses the correct entry point by setting the FLASK_APP environment variable:

On Linux/Mac:

```bash
export FLASK_APP=flasky.py
```
On Windows:
```bash
set FLASK_APP=flasky.py
```
### Running the Application
Start the Flask development server with:
```bash
flask run
```

### Useful Git Tips

Before cleaning your repository of untracked files or directories, perform a dry run to see what will be removed:

```bash
git clean -n -d
```
If the output is as expected, remove the untracked files and directories with:
```bash
git clean -f -d
```

Credits: most of this I got from Flask Web Development Developing Web Applications With Python from Miguel Grinberg published by O'Reilly