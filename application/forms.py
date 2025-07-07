from flask_wtf import FlaskForm # type: ignore
from flask_wtf.file import FileField, FileAllowed # type: ignore
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,EmailField, IntegerField,SelectField # type: ignore
from wtforms.validators import DataRequired, Length, Email # type: ignore

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    description = TextAreaField('Book Description', validators=[DataRequired()])
    genre = SelectField('Genre', validators=[DataRequired()], choices=[('Fiction', 'Fiction'), ('Adventure', 'Adventure')
                                                                       ,('Academic', 'Academic'), ('Political', 'Political'),
                                                                       ('Comics', 'Comics'), ('Religious', 'Religious'), ('Other', 'Other')] )
    file = FileField('Upload Book', validators=[FileAllowed(['docx', 'epub', 'pdf'])])
    submit = SubmitField('Add')

class Search(FlaskForm):
    keyword = StringField('keyword')
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')