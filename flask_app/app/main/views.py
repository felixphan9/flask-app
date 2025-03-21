from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from flask import current_app as app
from .. import db, mail
from . import main
from ..models import User
from . import main
from .forms import EmailForm
from flask_login import current_user
from ..decorators import admin_required, permission_required
from ..models import Permission
from flask_login import login_required

@main.route('/')
def home():
    return render_template('index.html', user=current_user)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
        return "For comment moderators!"
