from flask import Blueprint, render_template, request, session, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

def db_connect():
    """Подключение к базе данных"""
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='maria_yusupova_knowledge_base',
        user='maria_yusupova_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    """Закрытие соединения с БД"""
    conn.commit()
    cur.close()
    conn.close()

# Главная страница
@lab5.route('/lab5')
@lab5.route('/lab5/')
def main():
    login = session.get('login')
    return render_template('lab5/lab5.html', login=login)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    
    cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
    db_close(conn, cur)
    
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or user['password'] != password:
        return render_template('lab5/login.html', error='Неверный логин или пароль')

    session['login'] = login
    return redirect('/lab5')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')