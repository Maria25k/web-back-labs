from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash  
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab55():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='alena_kvashnina_knowledge_base',
            user='alena_kvashnina_knowledge_base',
            password='210521'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните логин и пароль', real_name=real_name)
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT login FROM users WHERE login = ?;", (login,))
            
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует", real_name=real_name)
        
        password_hash = generate_password_hash(password)
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", 
                       (login, password_hash, real_name))
        else:
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                       (login, password_hash, real_name))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/register.html', error=f'Ошибка: {str(e)}', real_name=real_name)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?;", (login,))
            
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/login.html', error=f'Ошибка: {str(e)}')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')  
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                             error='Заполните название и текст статьи!',
                             title=title, article_text=article_text,
                             is_favorite=is_favorite, is_public=is_public)

    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
            
        user = cur.fetchone()
        if not user:
            return render_template('lab5/create_article.html', error='Пользователь не найден')
            
        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);", 
                        (user_id, title, article_text, is_favorite, is_public))
        else:
            cur.execute("INSERT INTO articles(login_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
                        (user_id, title, article_text, is_favorite, is_public))

        db_close(conn, cur)
        return redirect('/lab5/list')
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error=f'Ошибка: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
            
        user = cur.fetchone()
        
        if not user:
            return "Пользователь не найден", 400
            
        user_id = user["id"]

        # Любимые статьи выводятся первыми
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, title, article_text, is_favorite, is_public FROM articles WHERE user_id = %s ORDER BY is_favorite DESC, id DESC;", (user_id,))
        else:
            cur.execute("SELECT id, title, article_text, is_favorite, is_public FROM articles WHERE login_id = ? ORDER BY is_favorite DESC, id DESC;", (user_id,))
            
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles, login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка: {str(e)}", 500

# ПУБЛИЧНЫЕ СТАТЬИ (доступны всем)
@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, u.login, u.real_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.is_public = true 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
        else:
            cur.execute("""
                SELECT a.id, a.title, a.article_text, a.is_favorite, u.login, u.real_name 
                FROM articles a 
                JOIN users u ON a.login_id = u.id 
                WHERE a.is_public = 1 
                ORDER BY a.is_favorite DESC, a.id DESC;
            """)
            
        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('/lab5/public_articles.html', articles=articles, login=session.get('login'))
        
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка: {str(e)}", 500

# СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
@lab5.route('/lab5/users')
def all_users():
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
        else:
            cur.execute("SELECT login, real_name FROM users ORDER BY login;")
            
        users = cur.fetchall()
        db_close(conn, cur)
        return render_template('/lab5/users.html', users=users, login=session.get('login'))
        
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка: {str(e)}", 500

# СМЕНА ИМЕНИ И ПАРОЛЯ
@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        if request.method == 'GET':
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT real_name FROM users WHERE login = %s;", (login,))
            else:
                cur.execute("SELECT real_name FROM users WHERE login = ?;", (login,))
                
            user = cur.fetchone()
            current_name = user['real_name'] if user and user['real_name'] else ""
            db_close(conn, cur)
            return render_template('/lab5/profile.html', current_name=current_name, login=login)

        # Обработка POST запроса
        new_name = request.form.get('real_name', '')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        errors = []

        # Проверка текущего пароля если меняется пароль
        if new_password:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT password FROM users WHERE login = %s;", (login,))
            else:
                cur.execute("SELECT password FROM users WHERE login = ?;", (login,))
                
            user = cur.fetchone()
            
            if not check_password_hash(user['password'], current_password):
                errors.append("Текущий пароль неверен")
            
            if new_password != confirm_password:
                errors.append("Новый пароль и подтверждение не совпадают")
            
            if len(new_password) < 3:
                errors.append("Новый пароль должен быть не менее 3 символов")

        if errors:
            db_close(conn, cur)
            return render_template('/lab5/profile.html', 
                                 errors=errors, 
                                 current_name=new_name, 
                                 login=login)

        # Обновление данных
        if new_password:
            password_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name = %s, password = %s WHERE login = %s;", 
                           (new_name, password_hash, login))
            else:
                cur.execute("UPDATE users SET real_name = ?, password = ? WHERE login = ?;", 
                           (new_name, password_hash, login))
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name = %s WHERE login = %s;", (new_name, login))
            else:
                cur.execute("UPDATE users SET real_name = ? WHERE login = ?;", (new_name, login))

        db_close(conn, cur)
        return render_template('/lab5/profile_success.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('/lab5/profile.html', 
                             errors=[f'Ошибка: {str(e)}'], 
                             current_name=request.form.get('real_name', ''), 
                             login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        user_id = user["id"]

        if request.method == 'GET':
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM articles WHERE id = %s AND user_id = %s;", (article_id, user_id))
            else:
                cur.execute("SELECT * FROM articles WHERE id = ? AND login_id = ?;", (article_id, user_id))
            
            article = cur.fetchone()
            db_close(conn, cur)
            
            if not article:
                return "Статья не найдена", 404
                
            return render_template('lab5/edit_article.html', article=article)

        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM articles WHERE id = %s AND user_id = %s;", (article_id, user_id))
            else:
                cur.execute("SELECT * FROM articles WHERE id = ? AND login_id = ?;", (article_id, user_id))
            article = cur.fetchone()
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', 
                                 article=article, 
                                 error='Заполните название и текст статьи!')

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title = %s, article_text = %s, is_favorite = %s, is_public = %s WHERE id = %s AND user_id = %s;", 
                       (title, article_text, is_favorite, is_public, article_id, user_id))
        else:
            cur.execute("UPDATE articles SET title = ?, article_text = ?, is_favorite = ?, is_public = ? WHERE id = ? AND login_id = ?;", 
                       (title, article_text, is_favorite, is_public, article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
        
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка: {str(e)}", 500

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        user_id = user["id"]

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id = %s AND user_id = %s;", (article_id, user_id))
        else:
            cur.execute("DELETE FROM articles WHERE id = ? AND login_id = ?;", (article_id, user_id))
        
        db_close(conn, cur)
        return redirect('/lab5/list')
        
    except Exception as e:
        db_close(conn, cur)
        return f"Ошибка: {str(e)}", 500