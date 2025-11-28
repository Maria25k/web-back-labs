from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1

app = Flask (__name__)
app.register_blueprint (lab1)

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

flower_list = [
    {'name': 'орхидея', 'price': 500},
    {'name': 'роза', 'price': 6000}
]

@app.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flowers=flower_list)

@app.route('/lab2/add_flower', methods=['POST'])
def add_flower_post():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '')
    
    if name and price:
        try:
            flower_list.append({
                'name': name, 
                'price': int(price)
            })
            return redirect('/lab2/flowers')
        except ValueError:
            return "Цена должна быть числом", 400
    return "Заполните все поля", 400

@app.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')


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

    
