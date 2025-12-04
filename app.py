from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

not_found_log = []

@app.route("/")
@app.route("/index")
def index():
    lab1 = url_for("lab1")
    lab2 = url_for("lab2")
    lab3 = url_for("lab3")
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
            <li><a href="/lab3/">Третья лабораторная</a></li>
        </ul>
        <footer>
            <p>Юсупова Мария Леонидовна, ФБИ-34, 3 курс, 2025 год</p>
        </footer>
    </body>
    </html>
    """

@app.errorhandler(500)
def internal_error(err):
    return "Внутренняя ошибка сервера. Мы уже работаем над этим!", 500

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url
    
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url
    }
    not_found_log.append(log_entry)
    
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
                for entry in reversed(not_found_log[-20:])  
            ])}
        </div>
    </body>
    </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
   

    
