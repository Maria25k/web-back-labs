from flask import Blueprint, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='maria_yusupova_knowledge_base',
        user='maria_yusupova_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    
    cur.execute("SELECT login FROM users WHERE login=%s", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')

    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)