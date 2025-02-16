from flask import render_template, redirect, url_for, flash
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404