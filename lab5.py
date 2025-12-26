from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    if db_type == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='maria_yusupova_knowledge_base',
            user='maria_yusupova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    """Закрытие соединения с БД"""
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5')
@lab5.route('/lab5/')
def main():
    login = session.get('login')
    return render_template('lab5/lab5.html', login=login)

# РЕГИСТРАЦИЯ - безопасно
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    
    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password_hash))
    db_close(conn, cur)
    
    return render_template('lab5/success.html', login=login)

# ВХОД - безопасно
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()
    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or not check_password_hash(user['password'], password):
        return render_template('lab5/login.html', error='Неверный логин или пароль')

    session['login'] = login
    return redirect('/lab5')

# СОЗДАНИЕ СТАТЬИ - безопасно
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()

    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    user_id = user['id']

    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("""
        INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, article_text, False, False, 0))

    db_close(conn, cur)
    return redirect('/lab5')

# ВЫВОД СТАТЕЙ - безопасно
@lab5.route('/lab5/list')
def articles_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    user_id = user['id']

    # БЕЗОПАСНО: параметризованный запрос
    cur.execute("SELECT * FROM articles WHERE user_id=%s", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)

# ВЫХОД
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')