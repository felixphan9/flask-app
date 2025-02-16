from flask import Blueprint

main = Blueprint('main', __name__)

# The modules should be imported after the blueprint object is created, in order to avoid errors due to circular dependencies.
from . import views, errors

