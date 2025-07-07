from flask import Blueprint

reader = Blueprint('main', __name__)

from . import views
