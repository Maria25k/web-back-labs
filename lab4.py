from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)

tree_count = 0
users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'М'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Иванов', 'gender': 'М'},
    {'login': 'anna', 'password': '777', 'name': 'Анна Сидорова', 'gender': 'Ж'},
    {'login': 'maria', 'password': '888', 'name': 'Мария Кузнецова', 'gender': 'Ж'}
]

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Оба поля должны быть числами')

    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Оба поля должны быть числами')
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Оба поля должны быть числами')
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть нулями')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'plant':
        if tree_count < 10:
            tree_count += 1
    elif operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    
    return redirect('/lab4/tree')

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'user_name' in session
        user_name = session.get('user_name', '')
        login_value = session.get('login', '')
        return render_template('lab4/login.html', 
                               authorized=authorized, 
                               user_name=user_name,
                               login_value=login_value,
                               error='')

    login_input = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login_input:
        return render_template('lab4/login.html', 
                               authorized=False, 
                               user_name='',
                               login_value=login_input,
                               error='Не введён логин')

    if not password:
        return render_template('lab4/login.html', 
                               authorized=False, 
                               user_name='',
                               login_value=login_input,
                               error='Не введён пароль')

    user_found = None
    for user in users:
        if user['login'] == login_input and user['password'] == password:
            user_found = user
            break

    if user_found:
        session['login'] = login_input
        session['user_name'] = user_found['name']
        return redirect('/lab4/login')  

    return render_template('lab4/login.html', 
                           authorized=False, 
                           user_name='',
                           login_value=login_input,
                           error='Неверные логин и/или пароль')


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = None
    error = None
    snowflakes = 0
    message = ''
    
    if request.method == 'POST':
        temp_str = request.form.get('temperature', '').strip()
        
        if not temp_str:
            error = 'Ошибка: не задана температура'
        else:
            try:
                temperature = int(temp_str)
                
                if temperature < -12:
                    error = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    error = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    snowflakes = 3
                    message = f'Установлена температура: {temperature}°C'
                elif -8 <= temperature <= -5:
                    snowflakes = 2
                    message = f'Установлена температура: {temperature}°C'
                elif -4 <= temperature <= -1:
                    snowflakes = 1
                    message = f'Установлена температура: {temperature}°C'
                    
            except ValueError:
                error = 'Температура должна быть числом'
    
    return render_template('lab4/fridge.html', 
                          temperature=temperature, 
                          error=error, 
                          snowflakes=snowflakes,
                          message=message)