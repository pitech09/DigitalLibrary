from flask import (session,
                   request, flash, url_for, redirect, render_template)
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import login_user, current_user, login_required  # type: ignore
from flask_mail import Message, Mail  # type: ignore
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from . import admin
from .. import (login_manager, db)
from ..forms import RegistrationForm, LoginForm
from ..models import User