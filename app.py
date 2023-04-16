import os
import sqlite3

import required as required
from flask import render_template, Flask, redirect, request
from flask_wtf import FlaskForm
from wtforms import SubmitField
from data import db_session
from data.news import News
from forms.user import RegisterForm, LoginForm, Сreate_a_note, Main_page, Delet_a_note, Form_for_start_window
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# стартовая страница
@app.route("/")
@app.route('/start_window', methods=['GET', 'POST'])
def start_window():
    form = Form_for_start_window()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('start_window.html', title='Авторизация', form=form)


# страница для регистрации
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    global user
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


id_user_password = -1


# страница для входа в аккаунт
@app.route('/login', methods=['GET', 'POST'])
def login():
    global id_user_password
    form = LoginForm()
    if form.validate_on_submit():
        sqlite_connection = sqlite3.connect('db/blogs.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("""SELECT * from users""")
        records = cursor.fetchall()
        names = []
        hashed_passwords = []
        for i in range(len(records)):
            names.append(records[i][1])
            hashed_passwords.append(records[i][4])
        flag_authorization = False
        cursor.execute("""SELECT id from users WHERE name = ?""", (form.name.data,))
        id_user_name2 = cursor.fetchall()
        for i in range(len(records)):
            user = User(
                name=form.name.data,
                hashed_password=records[i][4]
            )
            if user.check_password(form.password.data):
                flag_authorization = True
                id_user_password = i + 1
                break
        id_user_name = []
        for i in id_user_name2:
            id_user_name.append(i[0])
        if (
                form.name.data not in names) or id_user_name == [] or id_user_name == [] or id_user_password == -1 or \
                id_user_password not in id_user_name:
            return render_template('login.html', title='Авторизация на Lapis',
                                   form=form,
                                   message="Неправильный или логин, или пароль, или такого пользователя не существует")
        if not flag_authorization:
            return render_template('login.html', title='Авторизация на Lapis',
                                   form=form,
                                   message="Неправильный или логин, или пароль, или такого пользователя не существует")

        return redirect('/main_page')
    return render_template('login.html', title='Регистрация', form=form)


# главная страница
@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    form = Main_page()
    sqlite_connection = sqlite3.connect('db/blogs.db')
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT title, content, hashtags from news WHERE user_id=?""", (id_user_password,))
    result = cursor.fetchall()
    find = request.form.get('find')
    nothing_found = ''
    # проверяем вбил ли пользователь в строку поиска
    if find == None:
        find = ''
    find = find.split('#')
    del find[0]
    for i in range(len(find)):
        if find[i][-1] == ' ':
            find[i] = find[i][:-1]
    cursor.execute("""SELECT id, hashtags from news WHERE user_id=?""", (id_user_password,))
    records = cursor.fetchall()
    id_to_search = []
    for i in range(len(records)):  # проверяем в каких записях есть введённые хештеги
        flag_for_hashtags = True
        for j in find:
            if j.lower() not in records[i][1].lower():
                flag_for_hashtags = False
                break
        if flag_for_hashtags:
            id_to_search.append(records[i][0])
    result = []
    for i in id_to_search:  # ищем все нужные записи
        cursor.execute("""SELECT title, content, hashtags, id from news WHERE user_id=? AND id=?""",
                       (id_user_password, i))
        records = cursor.fetchall()
        result.append(records[0])
    if id_to_search == []:
        nothing_found = 'Ничего не найдено'
    result.reverse()
    return render_template('main_page.html', records=result, form=form, nothing_found=nothing_found,
                           id_user_password=id_user_password)


# страница для создания заметок
@app.route('/create_a_note', methods=['GET', 'POST'])
def create_a_note():
    global id_user_password
    db_sess = db_session.create_session()
    form = Сreate_a_note()
    if form.validate_on_submit():
        news = News(title=form.heading.data, content=form.note.data,
                    user_id=id_user_password, hashtags=form.hashtags.data, is_private=False)
        db_sess.add(news)
        db_sess.commit()
        return redirect('/main_page')
    return render_template('create_a_note.html', title='main_page', form=form)


# страница для удаления заметок
@app.route('/delete_a_note', methods=['GET', 'POST'])
def delete_a_note():
    global id_user_password
    form = Delet_a_note()
    if form.validate_on_submit():
        sqlite_connection = sqlite3.connect('db/blogs.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("""DELETE from news WHERE id=? AND user_id=?""", (form.number.data, id_user_password))
        sqlite_connection.commit()
        return redirect('/main_page')
    return render_template('delete_a_note.html', title='delete_a_note', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    print(required[id])
