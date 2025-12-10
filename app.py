from flask import Flask, render_template, url_for 
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3 
from lab4 import lab4

app = Flask(__name__)
app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3) 
app.register_blueprint(lab4) 

@app.route("/")
@app.route("/index")
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
            <li><a href="/lab1/">Первая лабораторная</a></li>
            <li><a href="/lab2/">Вторая лабораторная</a></li>        
            <li><a href="/lab3/">Третья лабораторная</a></li> 
            <li><a href="/lab4/">Четвертая лабораторная</a></li>             
        </ul>
        <footer>
            <p>Юсупова Мария Леонидовна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)