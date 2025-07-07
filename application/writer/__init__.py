from flask import Blueprint

writer = Blueprint('writer', __name__)

from . import views
