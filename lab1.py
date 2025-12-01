from flask import Blueprint, request, url_for
lab1 = Blueprint ('lab1', __name__)                                      

@lab1.route("/lab1/author")
def author():
    name = "Юсупова Мария Леонидовна"
    group = "ФБИ-34"
    faculty = "ФБ"
    
    return """
    <!doctype html> 
        <html>
            <body>
                <p>Студент: """+ name + """</p>
                <p>Группа: """ + group + """</p>
                </p>Факультет: """+ faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
         </html>"""

@lab1.route('/lab1/image')
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
@lab1.route('/lab1/counter')
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

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
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

@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return "Счётчик сброшен. <a href='/lab1/counter'>Вернуться</a>"

@lab1.route('/')
@lab1.route('/index')
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

@lab1.route('/lab1/')
def lab():
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