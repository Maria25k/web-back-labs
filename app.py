from flask import Flask, url_for, request, redirect
import datetime
app = Flask (__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <!html>
             <body>
                 <hl>web-сервер на flask</hl>
                 <a href="/author">author</a>
             </body>
        <!html>"""

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
         </html>"""

@app.route('/image')
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <hl>Дуб</hl>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0
@app.route('/counter')
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
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")