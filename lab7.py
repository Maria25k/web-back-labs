from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

def init_db():
    conn = sqlite3.connect('films.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Добавляем тестовые данные, если таблица пустая
    c.execute('SELECT COUNT(*) FROM films')
    if c.fetchone()[0] == 0:
        films = [
            ("Time loop", "Петля времени", 2012, 
             "В недалеком будущем, где стали возможны путешествия во времени, некая корпорация убирает нежелательных людей, отправляя их в прошлое."),
            ("Little nothings of life", "Мелочи жизни", 2025,
             "«Мелочи жизни» — художественный фильм режиссёра Тима Милантса. Экранизация одноимённой книги Клэр Киган."),
            ("Alpha", "Альфа", 2018,
             "20 000 лет назад Земля была холодным и неуютным местом, в котором смерть подстерегала человека на каждом шагу.")
        ]
        c.executemany('INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)', films)
    
    conn.commit()
    conn.close()

# Инициализируем БД при импорте
init_db()

def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn

def validate_film_data(film_data):
    errors = {}
    
    # Проверка русского названия
    if not film_data.get('title_ru') or film_data['title_ru'].strip() == "":
        errors['title_ru'] = 'Русское название обязательно'
    
    # Проверка оригинального названия (если русское пустое)
    if not film_data.get('title_ru') and (not film_data.get('title') or film_data['title'].strip() == ""):
        errors['title'] = 'Оригинальное название обязательно, если русское название не указано'
    
    # Автозаполнение оригинального названия
    if (not film_data.get('title') or film_data['title'].strip() == "") and film_data.get('title_ru'):
        film_data['title'] = film_data['title_ru']
    
    # Проверка года
    try:
        year = int(film_data.get('year', 0))
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except (ValueError, TypeError):
        errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    description = film_data.get('description', '')
    if not description or description.strip() == "":
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors, film_data

@lab7.route('/lab7/')
def lab77():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    
    films_list = []
    for film in films:
        films_list.append({
            'id': film['id'],
            'title': film['title'],
            'title_ru': film['title_ru'],
            'year': film['year'],
            'description': film['description']
        })
    
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if film is None:
        return jsonify({"error": "Фильм не найден"}), 404
    
    return jsonify({
        'id': film['id'],
        'title': film['title'],
        'title_ru': film['title_ru'],
        'year': film['year'],
        'description': film['description']
    })

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = get_db_connection()
    result = conn.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    if result.rowcount == 0:
        return jsonify({"error": "Фильм не найден"}), 404
    
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film_data = request.get_json()
    
    # Валидация данных
    errors, film_data = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    conn = get_db_connection()
    result = conn.execute(
        'UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'], id)
    )
    conn.commit()
    
    if result.rowcount == 0:
        conn.close()
        return jsonify({"error": "Фильм не найден"}), 404
    
    # Получаем обновленный фильм
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return jsonify({
        'id': film['id'],
        'title': film['title'],
        'title_ru': film['title_ru'],
        'year': film['year'],
        'description': film['description']
    })

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    
    # Валидация данных
    errors, film_data = validate_film_data(film_data)
    if errors:
        return jsonify(errors), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'])
    )
    film_id = cursor.lastrowid
    conn.commit()
    
    # Получаем созданный фильм
    film = conn.execute('SELECT * FROM films WHERE id = ?', (film_id,)).fetchone()
    conn.close()
    
    return jsonify({
        'id': film['id'],
        'title': film['title'],
        'title_ru': film['title_ru'],
        'year': film['year'],
        'description': film['description']
    }), 201