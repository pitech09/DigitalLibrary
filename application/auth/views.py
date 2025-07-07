from flask import (session,
                   request, flash, url_for, redirect, render_template)
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import login_user, current_user, login_required  # type: ignore
from flask_mail import Message, Mail  # type: ignore
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError
import flask_bcrypt
from . import auth
from .. import (login_manager, db)
from ..forms import RegistrationForm, LoginForm
from ..models import User

@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')
    if user_type == 'reader':
        return User.query.get(int(user_id))
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and flask_bcrypt.check_password_hash(user.password, password):
                login_user(user)
                session['user_type'] = 'reader'
                return redirect(url_for('main.index'))
            else:
                flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            email = form.email.data
            hashed_password = flask_bcrypt.generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
