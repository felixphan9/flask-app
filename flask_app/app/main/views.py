from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from flask import current_app as app
from .. import db, mail
from . import main
from ..models import User
from . import main
from .forms import LoginForm, RegistrationForm, EmailForm
from flask_login import login_user, logout_user, login_required

@main.route('/')
def home():
    user = {"name": "Fukku", "role": "Developer"}
    return render_template('index.html', user=user)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)  # ✅ Uses checkbox value
            flash(f'Login successful for user {form.username.data}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()  # Logs out the user
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

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
