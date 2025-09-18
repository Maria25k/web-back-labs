from flask import Flask
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
