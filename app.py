from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask (__name__)

@app.route("/")
@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <hl>web-сервер на flask</hl>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }                                          

@app.route("/lab1/author")
def author():
    name = "Юсупова Мария Леонидовна"
    group = "ФБИ-34"
    faculty = "ФБ"
    
    return """<!doctype html> 
        <html>
            <body>
                <p>Студент: """+ name + """</p>
                <p>Группа: """ + group + """</p>
                </p>Факультет: """+ faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
         </html>"""

@app.route('/lab1/image')
def image():
    path = url_for('static', filename='oak.jpg')
    headers = {
        'Content-Language': 'ru',
        'X-Custom-Header': 'Hello',
        'X-Another-Header': 'World'
    }
    return f"""
    <!DOCTYPE html>
    <html><h1>Дуб</h1>
    <body>
        <img src="{path}">
    </body>
    </html>
    """, 200, headers

count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time.strftime('%Y-%m-%d %H:%M:%S') + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + client_ip + '''<br>
        <p><a href="/lab1/counter/clear">Сбросить счётчик</a></p>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано…</i></div>
    </body>
</html>
''', 201

@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return "Счётчик сброшен. <a href='/lab1/counter'>Вернуться</a>"

@app.route('/')
@app.route('/index')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTTP, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>HTTP, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
            <li><a href="/lab2/">Вторая лабораторная</a></li>        
        </ul>
        <footer>
            <p>Юсупова Мария Леонидовна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    """

@app.route('/lab1')
def lab1():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений...</p>
        <a href="/">На главную</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
        </ul>
    </body>
    </html>
    """

@app.route('/400')
def bad_request():
    return "400 Bad Request: Неверный запрос", 400

@app.route('/401')
def unauthorized():
    return "401 Unauthorized: Требуется аутентификация", 401

@app.route('/402')
def payment_required():
    return "402 Payment Required: Требуется оплата", 402

@app.route('/403')
def forbidden():
    return "403 Forbidden: Доступ запрещен", 403

@app.route('/405')
def method_not_allowed():
    return "405 Method Not Allowed: Метод не разрешен", 405

@app.route('/418')
def teapot():
    return "418 I'm a teapot: Я чайник", 418

@app.errorhandler(500)
def internal_error(err):
    return "Внутренняя ошибка сервера. Мы уже работаем над этим!", 500

@app.route('/break')
def break_server():
    return 1 / 0  # Вызовет 500 ошибку



# Доп задание
import datetime

# Глобальная переменная для хранения журнала 404 ошибок
not_found_log = []

@app.errorhandler(404)
def not_found(err):
    # Получаем информацию о запросе
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url
    
    # Добавляем запись в журнал
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url
    }
    not_found_log.append(log_entry)
    
    # Формируем HTML-страницу
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .header {{
                text-align: center;
                color: #dc3545;
                margin-bottom: 30px;
            }}
            .info {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .log {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .log-entry {{
                border-bottom: 1px solid #eee;
                padding: 8px 0;
                font-family: monospace;
            }}
            .log-entry:last-child {{
                border-bottom: none;
            }}
            a {{
                color: #007bff;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1> Страница не найдена</h1>
        </div>
        
        <div class="info">
            <h3>Информация о текущем запросе:</h3>
            <p><strong>IP-адрес:</strong> {client_ip}</p>
            <p><strong>Время запроса:</strong> {access_time}</p>
            <p><strong>Запрошенный URL:</strong> {requested_url}</p>
            <p><a href="/">Вернуться на главную</a></p>
        </div>
        
        <div class="log">
            <h3> Журнал обращений к несуществующим страницам:</h3>
            {"".join([
                f'<div class="log-entry">[{entry["time"]}] пользователь {entry["ip"]} зашёл на адрес: {entry["url"]}</div>'
                for entry in reversed(not_found_log[-20:])  # показываем последние 20 записей
            ])}
        </div>
    </body>
    </html>
    """, 404


@app.route('/lab2/a/')
def a():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/add_flower/<name>') 
def add_flower(name):
    flower_list.append (name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name } </p>
    <p>Всего цветов: {len(flower_list)} </p>
    <p>Полный список: {flower_list} </p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Мария Юсупова', 2, 'ФБИ-34', 3
    fruits = [
{'name': 'яблоки', 'price': 100},
{'name': 'груши', 'price': 120},
{'name': 'апельсины', 'price': 80},
{'name': 'мандарины', 'price': 95},
{'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template ('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных... "
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/add_flower/')
def add_flower_empty():
    return "Вы не задали имя цветка", 400

@app.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flowers=flower_list)

@app.route('/lab2/flowers/clear')
def clear_flowers():
    global flower_list
    flower_list.clear()
    return '''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a><br>
        <a href="/lab2/">Назад к лабораторной 2</a>
    </body>
    </html>
    '''
@app.route('/lab2/flowers/<int:flower_id>')
def show_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок не найден", 404
    return render_template('flower_detail.html', 
                         flower=flower_list[flower_id], 
                         flower_id=flower_id,
                         total=len(flower_list))

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'Сумма': a + b,
        'Разность': a - b,
        'Произведение': a * b,
        'Частное': a / b if b != 0 else 'Деление на ноль невозможно!',
        'Степень': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)


books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 350},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 283},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 416}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

# Список пород собак
dogs = [
    {'name': 'Лабрадор', 'image': 'labrador.jpg', 'description': 'Дружелюбная семейная собака, отличный пловец'},
    {'name': 'Немецкая овчарка', 'image': 'german_shepherd.jpg', 'description': 'Умная служебная порода, преданный защитник'},
    {'name': 'Такса', 'image': 'dachshund.jpg', 'description': 'Маленькая охотничья собака с длинным телом'},
    {'name': 'Бульдог', 'image': 'bulldog.jpg', 'description': 'Коренастая собака с характерной мордой'},
    {'name': 'Пудель', 'image': 'poodle.jpg', 'description': 'Умная порода с кудрявой шерстью, отличный компаньон'},
    {'name': 'Бигль', 'image': 'beagle.jpg', 'description': 'Охотничья собака с острым нюхом, очень активная'},
    {'name': 'Золотистый ретривер', 'image': 'golden_retriever.jpg', 'description': 'Добродушная собака с золотистой шерстью'},
    {'name': 'Сибирский хаски', 'image': 'husky.jpg', 'description': 'Ездовая собака с голубыми глазами, любит холод'},
    {'name': 'Доберман', 'image': 'doberman.jpg', 'description': 'Сильная и грациозная служебная порода'},
    {'name': 'Ротвейлер', 'image': 'rottweiler.jpg', 'description': 'Мощная собака с сильным защитным инстинктом'},
    {'name': 'Боксёр', 'image': 'boxer.jpg', 'description': 'Энергичная и игривая собака с выразительной мордой'},
    {'name': 'Джек-рассел-терьер', 'image': 'jack_russell.jpg', 'description': 'Маленькая, но очень активная и смелая собака'},
    {'name': 'Чихуахуа', 'image': 'chihuahua.jpg', 'description': 'Самая маленькая порода собак в мире'},
    {'name': 'Шпиц', 'image': 'spitz.jpg', 'description': 'Пушистая собака с лисьей мордочкой'},
    {'name': 'Мопс', 'image': 'pug.jpg', 'description': 'Маленькая собака с морщинистой мордой и курносым носом'},
    {'name': 'Колли', 'image': 'collie.jpg', 'description': 'Длинношерстная пастушья собака, известная по фильму "Лесси"'},
    {'name': 'Далматин', 'image': 'dalmatian.jpg', 'description': 'Собака с уникальным пятнистым окрасом'},
    {'name': 'Сенбернар', 'image': 'st_bernard.jpg', 'description': 'Крупная спасательная собака, очень добрая'},
    {'name': 'Шарпей', 'image': 'sharpei.jpg', 'description': 'Собака с многочисленными складками кожи'},
    {'name': 'Корги', 'image': 'corgi.jpg', 'description': 'Маленькая пастушья собака с короткими лапами'}
]

@app.route('/lab2/dogs')
def show_dogs():
    return render_template('dogs.html', dogs=dogs)
