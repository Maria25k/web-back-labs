from flask import Flask, url_for, request, redirect
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
    return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{url_for('static', filename='lab1.css')}?v=2">
        </head>
        <body>
            <h1>Дуб</h1>
            <img src="{path}">
        </body>
    </html>
    '''

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
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">На главную</a>
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
