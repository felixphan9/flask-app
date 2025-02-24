from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from flask import current_app as app
from .. import db, mail
from . import main
from ..models import User
from . import main
from .forms import EmailForm

@main.route('/')
def home():
    user = {"name": "Fukku", "role": "Developer"}
    return render_template('index.html', user=user)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('views.login'))
    return render_template('register.html', form=form)

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
