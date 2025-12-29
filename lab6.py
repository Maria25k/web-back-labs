from flask import Blueprint, render_template, request, session
import json

lab6 = Blueprint('lab6', __name__)

# Глобальная переменная с офисами
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 900 + i * 100})  # Цена разная для каждого офиса

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    request_id = data.get('id')
    login = session.get('login')
    
    # Метод info - получение информации о кабинетах
    if method == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': request_id
        }
    
    # Метод booking - бронирование кабинета
    elif method == 'booking':
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': request_id
            }
        
        office_number = data.get('params')
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:  # Если офис уже арендован
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office already rented'
                        },
                        'id': request_id
                    }
                
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': request_id
        }
    
    # Метод cancellation - снятие аренды
    elif method == 'cancellation':
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': request_id
            }
        
        office_number = data.get('params')
        
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:  # Если офис не арендован
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Office is not rented'
                        },
                        'id': request_id
                    }
                
                if office['tenant'] != login:  # Если пытается снять чужую аренду
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 5,
                            'message': 'You are not the tenant of this office'
                        },
                        'id': request_id
                    }
                
                office['tenant'] = ""
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                }
        
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': request_id
        }
    
    # Если метод неизвестен
    else:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        }