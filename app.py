from flask import Flask, render_template, url_for 
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


from lab1 import lab1
from lab2 import lab2
from lab3 import lab3 
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from rgz import rgz


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3) 
app.register_blueprint(lab4)
app.register_blueprint(lab5)  
app.register_blueprint(lab6)  
app.register_blueprint(lab7)  
app.register_blueprint(rgz)

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
            <li><a href="/lab5/">Пятая лабораторная</a></li>
            <li><a href="/lab6/">Шестая лабораторная</a></li>
            <li><a href="/lab7/">Седьмая лабораторная</a></li>
            <li><a href="/lab8/">Восьмая лабораторная</a></li>
            <li><a href="/lab9/">Девятая лабораторная</a></li>
            <li><a href="/rgz/">Расчетно графическое задание</a></li>             
        </ul>
        <footer>
            <p>Юсупова Мария Леонидовна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)