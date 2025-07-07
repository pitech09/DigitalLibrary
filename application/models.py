import pytz
from flask_login import UserMixin  # type: ignore
from itsdangerous import TimedSerializer
from flask import current_app
from pygments.lexer import default

from . import login_manager, db
from zoneinfo import ZoneInfo
import secrets
from datetime import datetime
from flask_migrate import Migrate  # type: ignore

def get_localTime(self):
    tz = pytz.timezone("Africa/Johannesburg")
    return datetime.now(tz)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    shelf = db.relationship('Shelf', back_populates='user')
    book = db.relationship('Book', back_populates='user')

class Book(db.Model):
    __searchable__ = ['genre', 'description', 'title', 'author']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), default='Other')
    rating_count = db.Column(db.Integer, default=0)
    rating_total = db.Column(db.Integer, default=0)
    shelf_items = db.relationship('ShelfItem', backref='book', lazy=True)
    user = db.relationship('User', back_populates='book')
    filepath = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_book_user'), nullable=False)

class Shelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', name='fk_shelfuser'), nullable=False)
    date_created = db.Column(db.DateTime, default=get_localTime)
    shelf_items = db.relationship('ShelfItem', backref='shelf', lazy=True)
    user = db.relationship('User', back_populates='shelf')

class ShelfItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelf_id = db.Column(db.ForeignKey('shelf.id'), nullable=False)
    book_id = db.Column(db.ForeignKey('book.id', name='fk_shelfitem_id'), nullable=False)


