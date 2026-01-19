from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора», каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а саморазрушение — единственное, ради чего стоит жить."
    },
    {
        "title": "Léon",
        "title_ru": "Леон",
        "year": 1994,
        "description": "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, семья которой расстреляна коррумпированными полицейскими."
    }
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(films[id])

@lab7.route('/lab7/api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    del films[id]
    return "", 204

@lab7.route('/lab7/api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    
    film = request.get_json()
    
    # Проверка описания
    if not film.get('description') or len(film.get('description', '').strip()) == 0:
        return jsonify({"error": "Описание обязательно", "field": "description"}), 400
    
    # Проверка русского названия
    if not film.get('title_ru') or len(film.get('title_ru', '').strip()) == 0:
        return jsonify({"error": "Русское название обязательно", "field": "title_ru"}), 400
    
    # Если русское название есть, а оригинальное пустое, копируем русское в оригинальное
    if film.get('title_ru') and (not film.get('title') or len(film.get('title', '').strip()) == 0):
        film['title'] = film['title_ru']
    
    # Проверка года
    year = film.get('year')
    try:
        year = int(year)
        if year < 1895 or year > 2025:
            return jsonify({"error": "Год должен быть от 1895 до 2025", "field": "year"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Год должен быть числом", "field": "year"}), 400
    
    # Проверка длины описания
    if len(film.get('description', '')) > 2000:
        return jsonify({"error": "Описание не должно превышать 2000 символов", "field": "description"}), 400
    
    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверка описания
    if not film.get('description') or len(film.get('description', '').strip()) == 0:
        return jsonify({"error": "Описание обязательно", "field": "description"}), 400
    
    # Проверка русского названия
    if not film.get('title_ru') or len(film.get('title_ru', '').strip()) == 0:
        return jsonify({"error": "Русское название обязательно", "field": "title_ru"}), 400
    
    # Если русское название есть, а оригинальное пустое, копируем русское в оригинальное
    if film.get('title_ru') and (not film.get('title') or len(film.get('title', '').strip()) == 0):
        film['title'] = film['title_ru']
    
    # Проверка года
    year = film.get('year')
    try:
        year = int(year)
        if year < 1895 or year > 2025:
            return jsonify({"error": "Год должен быть от 1895 до 2025", "field": "year"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Год должен быть числом", "field": "year"}), 400
    
    # Проверка длины описания
    if len(film.get('description', '')) > 2000:
        return jsonify({"error": "Описание не должно превышать 2000 символов", "field": "description"}), 400
    
    films.append(film)
    return jsonify({"id": len(films) - 1})