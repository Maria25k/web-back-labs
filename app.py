from flask import Flask, url_for
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
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''