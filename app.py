from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user, login_manager
import os
import flask_bcrypt
from flask_migrate import Migrate
from form import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', name='fk_bookidtouser'))
    book = db.relationship('Book', back_populates='user')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    genre = db.Column(db.String(40), default='Other')
    rating_count = db.Column(db.Integer, default=0)
    rating_total = db.Column(db.Integer, default=0)
    user = db.relationship('User', back_populates='book')
    filepath = db.Column(db.String(200), nullable=False)



    @property
    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return round(self.rating_total/self.rating_count, 1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/rate/<int:book_id>', methods=['POST', 'GET'])
@login_required
def rate(book_id):

    book = Book.query.get_or_404(book_id)
    if current_user.book_id == book_id:
       flash('You have already rated this book')
       return redirect(url_for('books'))
    rating = int(request.form['rating'])
    current_user.book_id = book.id
    book.rating_total +=rating
    book.rating_count +=1
    db.session.commit()
    return redirect(url_for('books'))



@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and flask_bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
    return render_template('login.html', form=form)




@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/upload', methods=['GET', 'POST'])
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_book = Book(title=title, filepath=file.filename, description=description, author=author, genre=genre)
            db.session.add(new_book)
            db.session.commit()
            flash('Book uploaded successfully.')
            return redirect(url_for('index'))

    return render_template('uploads.html', form=form)

@app.route('/books', methods=['GET', 'POST'])
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/download/<int:book_id>')
def download(book_id):
    book = Book.query.get_or_404(book_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], book.filepath)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=7777,debug=True)