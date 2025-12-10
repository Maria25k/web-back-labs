from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='alena_kvashnina_knowledge_base',
            user='alena_kvashnina_knowledge_base',
            password='210521'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/')
def lab66():  
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/login')
def login():
    session['login'] = 'test_user'
    return 'Вы авторизованы как test_user. <a href="/lab6/">Вернуться к офисам</a>'

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        try:
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
            offices = cur.fetchall()
            db_close(conn, cur)
            
            offices_list = []
            for office in offices:
                offices_list.append({
                    'number': office['number'],
                    'tenant': office['tenant'] if office['tenant'] else '',
                    'price': office['price']
                })
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': f'Ошибка БД: {str(e)}'}, 'id': id}
    
    login_user = session.get('login')
    if not login_user:
        return {'jsonrpc': '2.0', 'error': {'code': 1, 'message': 'Неавторизованный пользователь'}, 'id': id}
    
    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        try:
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {'jsonrpc': '2.0', 'error': {'code': -32602, 'message': 'Офис не найден'}, 'id': id}
            
            if office['tenant']:
                db_close(conn, cur)
                return {'jsonrpc': '2.0', 'error': {'code': 2, 'message': 'Офис уже арендован'}, 'id': id}
            
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login_user, office_number))
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'result': 'success', 'id': id}
            
        except Exception as e:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': f'Ошибка БД: {str(e)}'}, 'id': id}
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        conn, cur = db_connect()
        try:
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
            office = cur.fetchone()
            
            if not office:
                db_close(conn, cur)
                return {'jsonrpc': '2.0', 'error': {'code': -32602, 'message': 'Офис не найден'}, 'id': id}
            
            if not office['tenant']:
                db_close(conn, cur)
                return {'jsonrpc': '2.0', 'error': {'code': 3, 'message': 'Офис не арендован'}, 'id': id}
            
            if office['tenant'] != login_user:
                db_close(conn, cur)
                return {'jsonrpc': '2.0', 'error': {'code': 4, 'message': 'Можно освободить только свой офис'}, 'id': id}
            
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", ("", office_number))
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'result': 'success', 'id': id}
            
        except Exception as e:
            db_close(conn, cur)
            return {'jsonrpc': '2.0', 'error': {'code': -32000, 'message': f'Ошибка БД: {str(e)}'}, 'id': id}
    
    return {'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Метод не найден'}, 'id': id}