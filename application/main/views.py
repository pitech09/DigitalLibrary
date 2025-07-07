from flask import (session, current_app,
                   request, flash, url_for, redirect, render_template, send_from_directory)
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import login_user, current_user, login_required, logout_user  # type: ignore
from flask_mail import Message, Mail  # type: ignore
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError
import os
from . import reader
from .. import (login_manager, db)
from ..forms import Search, BookForm
from ..models import Book, User


@reader.route('/', methods=['GET', 'POST'])
@reader.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')

@reader.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = BookForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            title = form.title.data
            description = form.description.data
            author = form.author.data
            file = form.file.data
            genre = form.genre.data

            file.save(os.path.join(current_app.config['UPLOAD_PATH'], file.filename))
            new_book = Book(title=title, filepath=file.filename, description=description, author=author, genre=genre)
            new_book.user_id = current_user.id
            db.session.add(new_book)
            db.session.commit()
            flash('Book uploaded successfully.')
            return redirect(url_for('main.index'))

    return render_template('main/uploads.html', form=form)

@reader.route('/books', methods=['GET', 'POST'])
def books():
    form1 = Search()
    books = Book.query.all()
    return render_template('main/books.html', books=books, form1=form1)

@reader.route('/download/<int:book_id>')
def download(book_id):
    book = Book.query.get_or_404(book_id)
    if book:
        print('book found', current_app.config['UPLOAD_PATH'])
        print(book.filepath)
    return send_from_directory(current_app.config['UPLOAD_PATH'], book.filepath)

@reader.route('/search', methods=['POST', 'GET'])
def search():
    form1 = Search()
    keyword = form1.keyword.data
    books = Book.query.filter(
        Book.genre.like(f'%{keyword}%') |
        Book.description.like(f'%{keyword}%') |
        Book.title.like(f'%{keyword}%') |
        Book.author.like(f'%{keyword}%')
    )
    return render_template('main/books.html', books=books, form1=form1)


@reader.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
