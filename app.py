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

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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

@app.errorhandler(404)
def not_found(err):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body { text-align: center; padding: 50px; }
            h1 { color: red; }
        </style>
    </head>
    <body>
        <h1>Ой! Страница не найдена.</h1>
        <p>Вернитесь на <a href="/">главную</a>.</p>
        <img src="/static/oak1.jpg" width="300">
    </body>
    </html>
    """, 404

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
    name = 'Петров Иван'
    return render_template('example.html', name=name)