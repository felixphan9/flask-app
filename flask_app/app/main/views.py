from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from flask import current_app as app
from .. import db, mail
from . import main
from ..models import User
from . import main
from .forms import EmailForm
from flask_login import current_user

@main.route('/')
def home():
    return render_template('index.html', user=current_user)

@main.route('/email', methods=['GET', 'POST'])
def email():
    form = EmailForm()
    if form.validate_on_submit():
        msg = Message(
            subject="Test Email from Flask",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[form.email.data],
            body="Hello! This is a test email sent from Flask-Mail."
        )
        try:
            mail.send(msg)
            flash('✅ Email sent successfully!', 'success')
        except Exception as e:
            flash(f'❌ An error occurred: {e}', 'danger')
        return redirect(url_for('views.email'))
    return render_template('email.html', form=form)
