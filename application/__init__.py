from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_login import LoginManager  # type: ignore
from config import *
from flask_mail import Mail  # type: ignore

# from flask_socketio import SocketIO, emit

db = SQLAlchemy()
# socketio = SocketIO()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "auth.login"
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    UPLOAD_PATH = os.path.join(basedir, 'static', 'books')

    os.makedirs(UPLOAD_PATH, exist_ok=True)

    login_manager.init_app(app)
    app.config['UPLOAD_PATH'] = UPLOAD_PATH

    db.init_app(app)
    socketio.init_app(app)

    mail = Mail(app)
    mail.init_app(app)

    # routes will go here
    # blueprint registration

    from .main import reader as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .writer import writer as writer_blueprint
    app.register_blueprint(writer_blueprint, url_prefix='/writer')


    return app
