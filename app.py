from flask import Flask, render_template, url_for
from flask_login import LoginManager
import datetime
import os
from os import path
from dotenv import load_dotenv

load_dotenv()

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from rgz import rgz
from db import db
from db.models import users

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')

# Настройка соединения с БД
if app.config['DB_TYPE'] == 'postgres':
    db_name = os.environ.get('DB_NAME', 'ivan_ivanov_orm')
    db_user = os.environ.get('DB_USER', 'ivan_ivanov_orm')
    db_password = os.environ.get('DB_PASSWORD', '123')
    host_ip = os.environ.get('DB_HOST', '127.0.0.1')
    host_port = os.environ.get('DB_PORT', '5432')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация БД
db.init_app(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Регистрация Blueprint'ов
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(rgz)

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

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