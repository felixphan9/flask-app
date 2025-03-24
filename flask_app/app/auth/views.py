from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from . import auth
from flask_login import current_user
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from flask_mail import Message
from flask import current_app
from app import mail

@auth.before_app_request
def before_request():
    '''This handler will intercept a request when three conditions are met:
    1. The request is not for a static file (the URL starts with /static/).
    2. The user is authenticated (logged in).
    3. The user has not confirmed their account yet.
    If these conditions are met, the user is redirected to the unconfirmed page.'''  
    # Ping the current user to perform session management or any necessary checks
    if current_user.is_authenticated:
        current_user.ping()  # Ensure the user session is valid (if your app uses this method)

    # Check if the user is authenticated, unconfirmed, and not accessing static or auth routes
    if current_user.is_authenticated and not current_user.confirmed \
            and request.blueprint != 'auth' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if email is correct and password is valid
        user = User.query.filter_by(email=form.email.data).first()  # Use email to query the user
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)  # ✅ Uses checkbox value
            flash(f'Login successful for user {form.username.data}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username already
        user_exists = User.query.filter_by(username=form.username.data).first()
        email_exists = User.query.filter_by(email=form.email.data).first()

        if user_exists:
            flash('Username already exists. Please choose a different one.', 'danger')
        elif email_exists:
            flash('Email already registered. Please choose a different one.', 'danger')
        else:
            # Create a new user
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)

            # Generate a token for the user
            token = new_user.get_token(expires_in=3600)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            subject = "Please confirm your email"
            body = f"Hi {new_user.username},\n\nPlease click the link below to confirm your email address:\n{confirm_url}\n\nThank you!"
            
            msg = Message(subject=subject,
                          sender=current_app.config['MAIL_DEFAULT_SENDER'],
                          recipients=[new_user.email],
                          body=body)
            try:
                mail.send(msg)
                flash('A confirmation email has been sent. Please check your inbox.', 'info')
                # Add the user to the database before sending the email
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                flash(f'An error occurred while sending the email: {e}', 'danger')
                return redirect(url_for('auth.register'))
            
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
def confirm_email(token):
    user = User.verify_token(token)
    if not user:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.register'))
    
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash('You have confirmed your account. Thank you!', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.get_token(expires_in=3600)
    print('token' , token)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    subject = "Reconfirm your email"
    body = f"Hi {current_user.username},\n\nPlease click the link below to re-confirm your email address:\n{confirm_url}\n\nThank you!"
    
    msg = Message(subject=subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[current_user.email],
                  body=body)
    try:
        mail.send(msg)
        flash('A new confirmation email has been sent to you by email.', 'info')
    except Exception as e:
        flash(f'An error occurred while sending the email: {e}', 'danger')
    
    return redirect(url_for('main.home'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    
    return render_template('auth/unconfirmed.html')
