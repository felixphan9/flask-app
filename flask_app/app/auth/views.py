from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db

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
            new_user = User(username=form.username.data, email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('main.home'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))