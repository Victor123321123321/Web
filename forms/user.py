from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SearchField, validators
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')

class Сreate_a_note(FlaskForm):
    heading = TextAreaField('Заголовок', validators=[DataRequired()])
    note = TextAreaField('Заметка', validators=[DataRequired()])
    hashtags = TextAreaField('Хештеги')

class Delet_a_note(FlaskForm):
    number = TextAreaField('Номер записи')

class Main_page(FlaskForm):
    search = SearchField('?????', validators=[DataRequired()])
    submit = SubmitField('Создать')

class Form_for_start_window(FlaskForm):
    submit = SubmitField('Войти')
    submit2 = SubmitField('Зарегистрироваться')