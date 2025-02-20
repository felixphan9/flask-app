from flask import Blueprint

main = Blueprint('main', __name__)
"""Blueprints are a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.""" 

# The modules should be imported after the blueprint object is created, in order to avoid errors due to circular dependencies.
from . import views, errors

