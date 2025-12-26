from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

rgz = Blueprint('rgz', __name__, template_folder='templates/rgz')

STUDENT_NAME = "Юсупова Мария Леонидовна"
STUDENT_GROUP = "ФБИ-34"

SERVICE_TYPES = [
    'программист', 'дизайнер', 'бухгалтер', 'репетитор', 'маркетолог',
    'переводчик', 'юрист', 'фотограф', 'тренер', 'визажист',
    'парикмахер', 'сантехник', 'электрик', 'водитель', 'няня'
]

DB_PATH = 'rgz.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        name TEXT NOT NULL,
        service_type TEXT NOT NULL,
        experience INTEGER NOT NULL,
        price INTEGER NOT NULL,
        about TEXT,
        is_hidden BOOLEAN DEFAULT 0
    )
    ''')
    
    # Администратор
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_hash = generate_password_hash('admin123')
        cursor.execute('''
        INSERT INTO users (username, password_hash, role, name, service_type, experience, price, about, is_hidden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', admin_hash, 'admin', 'Администратор', 'администрация', 10, 0, 'Администратор сайта', 0))
    
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    
    if count < 31:  
        test_users = [
            ('user1', 'password1', 'Иван Петров', 'программист', 5, 2000, 'Разработчик Python'),
            ('user2', 'password2', 'Мария Сидорова', 'дизайнер', 3, 1500, 'UI/UX дизайнер'),
            ('user3', 'password3', 'Алексей Иванов', 'бухгалтер', 10, 1800, 'Бухгалтерский учёт'),
            ('user4', 'password4', 'Елена Козлова', 'репетитор', 7, 1200, 'Преподаватель математики'),
            ('user5', 'password5', 'Дмитрий Смирнов', 'маркетолог', 4, 1700, 'SMM специалист'),
            ('user6', 'password6', 'Ольга Новикова', 'переводчик', 6, 1300, 'Переводчик английского'),
            ('user7', 'password7', 'Сергей Кузнецов', 'юрист', 8, 2200, 'Юридические консультации'),
            ('user8', 'password8', 'Анна Морозова', 'фотограф', 2, 1000, 'Фотосъёмка'),
            ('user9', 'password9', 'Павел Волков', 'тренер', 5, 1400, 'Фитнес-тренер'),
            ('user10', 'password10', 'Татьяна Зайцева', 'визажист', 4, 900, 'Визажист'),
            ('user11', 'password11', 'Михаил Попов', 'парикмахер', 6, 800, 'Стилист'),
            ('user12', 'password12', 'Екатерина Лебедева', 'сантехник', 8, 1500, 'Сантехнические работы'),
            ('user13', 'password13', 'Андрей Ковалев', 'электрик', 7, 1600, 'Электромонтаж'),
            ('user14', 'password14', 'Наталья Федорова', 'водитель', 10, 1200, 'Частный водитель'),
            ('user15', 'password15', 'Олег Орлов', 'няня', 3, 700, 'Няня для детей'),
            ('user16', 'password16', 'Ирина Медведева', 'сиделка', 5, 900, 'Уход за пожилыми'),
            ('user17', 'password17', 'Владимир Алексеев', 'уборщик', 2, 600, 'Клининг'),
            ('user18', 'password18', 'Светлана Николаева', 'ремонтник', 4, 1800, 'Ремонт квартир'),
            ('user19', 'password19', 'Константин Захаров', 'консультант', 6, 1400, 'Бизнес-консультант'),
            ('user20', 'password20', 'Людмила Тихонова', 'программист', 4, 1900, 'Frontend разработчик'),
            ('user21', 'password21', 'Геннадий Семенов', 'дизайнер', 5, 1600, 'Графический дизайнер'),
            ('user22', 'password22', 'Валентина Петрова', 'бухгалтер', 12, 2000, 'Главный бухгалтер'),
            ('user23', 'password23', 'Борис Фролов', 'репетитор', 8, 1300, 'Репетитор физики'),
            ('user24', 'password24', 'Зоя Макарова', 'маркетолог', 5, 1800, 'Digital маркетинг'),
            ('user25', 'password25', 'Евгений Егоров', 'переводчик', 7, 1500, 'Технический перевод'),
            ('user26', 'password26', 'Галина Волкова', 'юрист', 9, 2400, 'Семейное право'),
            ('user27', 'password27', 'Станислав Соловьев', 'фотограф', 3, 1100, 'Портретная съёмка'),
            ('user28', 'password28', 'Лидия Васильева', 'тренер', 6, 1500, 'Йога инструктор'),
            ('user29', 'password29', 'Артем Павлов', 'визажист', 5, 1000, 'Вечерний макияж'),
            ('user30', 'password30', 'Виктория Семенова', 'парикмахер', 7, 900, 'Парикмахер-стилист'),
        ]
        
        for username, password, name, service, exp, price, about in test_users[:10]:  
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if not cursor.fetchone():
                password_hash = generate_password_hash(password)
                cursor.execute('''
                INSERT INTO users (username, password_hash, name, service_type, experience, price, about, is_hidden)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (username, password_hash, name, service, exp, price, about, 0))
    
    conn.commit()
    conn.close()

@rgz.context_processor
def add_info():
    return {
        'student_name': STUDENT_NAME,
        'student_group': STUDENT_GROUP,
        'service_types': SERVICE_TYPES
    }

# Декоратор для проверки прав администратора
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('rgz.login'))
        if session.get('role') != 'admin':
            return "Доступ запрещен. Требуются права администратора.", 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@rgz.route('/rgz')
@rgz.route('/rgz/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE is_hidden = 0 ORDER BY id DESC LIMIT 5")
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['name'] = user['name']
            return redirect(url_for('rgz.profile'))
        
        return render_template('login.html', error='Неверный логин или пароль')
    
    return render_template('login.html')

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        service_type = request.form['service_type']
        experience = request.form['experience']
        price = request.form['price']
        about = request.form.get('about', '')

        if not re.match(r'^[a-zA-Z0-9_\.-]+$', username):
            return render_template('register.html', error='Неверный формат логина')
        if not re.match(r'^[a-zA-Z0-9_\.-]+$', password):
            return render_template('register.html', error='Неверный формат пароля')

        try:
            exp = int(experience)
            prc = int(price)
            if exp < 0 or prc <= 0:
                return render_template('register.html', error='Неверные данные')
        except:
            return render_template('register.html', error='Неверные данные')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error='Пользователь уже существует')

        password_hash = generate_password_hash(password)
        cursor.execute('''
        INSERT INTO users (username, password_hash, name, service_type, experience, price, about)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, name, service_type, exp, prc, about))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()

        session['user_id'] = user_id
        session['username'] = username
        session['role'] = 'user'
        session['name'] = name
        return redirect(url_for('rgz.profile'))

    return render_template('register.html')

@rgz.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        session.clear()
        return redirect(url_for('rgz.login'))
    
    return render_template('profile.html', user=user)

@rgz.route('/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))
    
    name = request.form['name']
    service_type = request.form['service_type']
    experience = int(request.form['experience'])
    price = int(request.form['price'])
    about = request.form.get('about', '')
    is_hidden = 'is_hidden' in request.form
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users 
    SET name=?, service_type=?, experience=?, price=?, about=?, is_hidden=?
    WHERE id=?
    ''', (name, service_type, experience, price, about, 1 if is_hidden else 0, session['user_id']))
    conn.commit()
    conn.close()
    
    session['name'] = name
    return redirect(url_for('rgz.profile'))

@rgz.route('/delete')
def delete():
    if 'user_id' not in session:
        return redirect(url_for('rgz.login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    
    session.clear()
    return redirect(url_for('rgz.index'))

@rgz.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('rgz.index'))

@rgz.route('/admin')
@admin_required
def admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', users=users)

@rgz.route('/admin/delete/<int:user_id>')
@admin_required
def admin_delete(user_id):
    """Удаление пользователя администратором"""
    
    if user_id == session['user_id']:
        return redirect(url_for('rgz.admin'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user and user['role'] == 'admin':
        return redirect(url_for('rgz.admin'))
    
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('rgz.admin'))

@rgz.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Редактирование пользователя администратором"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        role = request.form['role']
        service_type = request.form['service_type']
        
        try:
            experience = int(request.form['experience'])
            price = int(request.form['price'])
        except:
            return "Неверный формат данных", 400
        
        about = request.form.get('about', '')
        is_hidden = 'is_hidden' in request.form
        
        # Проверяем уникальность логина
        cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
        if cursor.fetchone():
            conn.close()
            return "Логин уже занят", 400
        
        cursor.execute('''
        UPDATE users 
        SET name=?, username=?, role=?, service_type=?, experience=?, price=?, about=?, is_hidden=?
        WHERE id=?
        ''', (name, username, role, service_type, experience, price, about, 1 if is_hidden else 0, user_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('rgz.admin'))
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return "Пользователь не найден", 404
    
    return render_template('admin_edit.html', user=user)

@rgz.route('/search')
def search():
    name = request.args.get('name', '')
    service = request.args.get('service', '')
    exp_min = request.args.get('exp_min', 0, type=int)
    exp_max = request.args.get('exp_max', 100, type=int)
    price_min = request.args.get('price_min', 0, type=int)
    price_max = request.args.get('price_max', 10000, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM users WHERE is_hidden = 0"
    params = []
    
    if name:
        query += " AND name LIKE ?"
        params.append(f'%{name}%')
    if service:
        query += " AND service_type LIKE ?"
        params.append(f'%{service}%')
    
    query += " AND experience >= ? AND experience <= ?"
    params.extend([exp_min, exp_max])
    
    query += " AND price >= ? AND price <= ?"
    params.extend([price_min, price_max])
    
    query += " LIMIT 10"
    
    cursor.execute(query, params)
    users = cursor.fetchall()
    conn.close()
    
    result = []
    for user in users:
        result.append({
            'id': user['id'],
            'name': user['name'],
            'service_type': user['service_type'],
            'experience': user['experience'],
            'price': user['price'],
            'about': user['about']
        })
    
    return jsonify(result)