from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path

lab5 = Blueprint('lab5', __name__)

def db_connect():
    """Подключение к БД в зависимости от типа"""
    db_type = current_app.config.get('DB_TYPE', 'postgres')
    
    if db_type == 'postgres':
        # PostgreSQL
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

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '')  

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    
    cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s)", 
            (login, password_hash, real_name))
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

    if not user or not check_password_hash(user['password'], password):
        return render_template('lab5/login.html', error='Неверный логин или пароль')

    session['login'] = login
    return redirect('/lab5')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # ВАЛИДАЦИЯ: проверка на пустые поля и пробелы
    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Название и текст статьи не могут быть пустыми')
    if len(title.strip()) == 0 or len(article_text.strip()) == 0:
        return render_template('lab5/create_article.html', error='Название и текст статьи не могут состоять только из пробелов')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    user_id = user['id']

    cur.execute("""
        INSERT INTO articles (user_id, title, article_text, is_favorite, is_public, likes) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, article_text, False, False, 0))

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def articles_list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    cur.execute("SELECT id FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    
    if not user:  
        db_close(conn, cur)
        return redirect('/lab5') 
    user_id = user['id']  

    cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC", (user_id,))
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles, login=login)
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=%s", (article_id,))
    article = cur.fetchone()
    
    if not article or article['login'] != login:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                              article=article, 
                              error='Заполните все поля')

    cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s", 
                (title, article_text, article_id))
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    cur.execute("SELECT a.*, u.login FROM articles a JOIN users u ON a.user_id = u.id WHERE a.id=%s", (article_id,))
    article = cur.fetchone()
    
    if article and article['login'] == login:
        cur.execute("DELETE FROM articles WHERE id=%s", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def all_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    cur.execute("SELECT login, real_name FROM users ORDER BY login")
    users = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/all_users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    if request.method == 'GET':
        cur.execute("SELECT real_name FROM users WHERE login=%s", (login,))
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', real_name=user['real_name'])

    # POST - сохранение изменений
    new_real_name = request.form.get('real_name')
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    cur.execute("SELECT password FROM users WHERE login=%s", (login,))
    user = cur.fetchone()
    
    error = None
    
    if new_password:
        if not check_password_hash(user['password'], current_password):
            error = 'Текущий пароль неверен'
        elif new_password != confirm_password:
            error = 'Новый пароль и подтверждение не совпадают'
        elif len(new_password) < 3:
            error = 'Новый пароль слишком короткий'
        else:
            new_password_hash = generate_password_hash(new_password)
            cur.execute("UPDATE users SET password=%s WHERE login=%s", 
                       (new_password_hash, login))
    
    if not error:
        cur.execute("UPDATE users SET real_name=%s WHERE login=%s", 
                   (new_real_name, login))
    
    db_close(conn, cur)
    
    if error:
        return render_template('lab5/profile.html', 
                              real_name=new_real_name, 
                              error=error)
    
    return redirect('/lab5')

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    cur.execute("""
        SELECT a.*, u.login as author 
        FROM articles a 
        JOIN users u ON a.user_id = u.id 
        WHERE a.is_public = TRUE 
        ORDER BY a.likes DESC
    """)
    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/public_articles.html', 
                          articles=articles, 
                          login=session.get('login'))
