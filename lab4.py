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
        return render_template('lab4/login.html', authorized=authorized, user_name=user_name)

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '')


    if login == '':
        return render_template('lab4/login.html', error='Не введён логин', login_value=login)

    if password == '':
        return render_template('lab4/login.html', error='Не введён пароль', login_value=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['user_name'] = user['name']
            return redirect('/lab4/login')

    return render_template('lab4/login.html', error='Неверные логин и/или пароль', login_value=login)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
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

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    grains = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }
    
    if request.method == 'GET':
        return render_template('lab4/grain.html', grains=list(grains.keys()))
    
    grain_type = request.form.get('grain')
    weight_str = request.form.get('weight', '').strip()
    
    errors = []
    
    if not grain_type:
        errors.append('Не выбран тип зерна')
    
    if not weight_str:
        errors.append('Не указан вес')
    else:
        try:
            weight = float(weight_str)
            if weight <= 0:
                errors.append('Вес должен быть положительным числом')
            elif weight > 100:
                errors.append('Такого объёма сейчас нет в наличии')
        except ValueError:
            errors.append('Вес должен быть числом')
    
    if errors:
        return render_template('lab4/grain.html', 
                              grains=list(grains.keys()),
                              errors=errors)
    
    weight = float(weight_str)
    price_per_ton = grains[grain_type]
    total = weight * price_per_ton
    
    discount = 0
    if weight > 10:
        discount = total * 0.10
        total -= discount
    
    return render_template('lab4/grain_result.html',
                          grain=grain_type,
                          weight=weight,
                          price_per_ton=price_per_ton,
                          total=total,
                          discount=discount,
                          has_discount=discount > 0)

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    global users
    if request.method == 'GET':
        return render_template('lab4/register.html')

    login = (request.form.get('login') or '').strip()
    name = (request.form.get('name') or '').strip()
    password = request.form.get('password') or ''
    password2 = request.form.get('password2') or ''

    if not login:
        return render_template('lab4/register.html', error='Не введён логин', entered_login=login, entered_name=name)
    if not name:
        return render_template('lab4/register.html', error='Не введено имя', entered_login=login, entered_name=name)
    if not password:
        return render_template('lab4/register.html', error='Не введён пароль', entered_login=login, entered_name=name)
    if password != password2:
        return render_template('lab4/register.html', error='Пароли не совпадают', entered_login=login, entered_name=name)

    for u in users:
        if u.get('login') == login:
            return render_template('lab4/register.html', error='Логин уже используется', entered_login=login, entered_name=name)

    users.append({'login': login, 'password': password, 'name': name, 'gender': ''})
    return redirect('/lab4/login')



@lab4.route('/lab4/users', methods=['GET'])
def users_page():
    if 'user_name' not in session:
        return redirect('/lab4/login')

    me_name = session['user_name']
    me = None
    for u in users:
        if u.get('name') == me_name:
            me = u
            break

    users_public = [{'login': u['login'], 'name': u['name']} for u in users]
    return render_template('lab4/users.html', users=users_public, me_login=(me['login'] if me else None))


@lab4.route('/lab4/delete_self', methods=['POST'])
def delete_self():
    global users
    if 'user_name' not in session:
        return redirect('/lab4/login')

    current_name = session.get('user_name')
    users = [u for u in users if u.get('name') != current_name]
    session.pop('user_name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_profile():
    global users
    if 'user_name' not in session:
        return redirect('/lab4/login')

    current_name = session['user_name']
    user = None
    for u in users:
        if u.get('name') == current_name:
            user = u
            break

    if user is None:
        return redirect('/lab4/login')

    
    if request.method == 'GET':
        return render_template('lab4/edit.html', user_public={'login': user['login'], 'name': user['name']})

  
    new_login = (request.form.get('login') or '').strip()
    new_name = (request.form.get('name') or '').strip()
    new_pass = request.form.get('password') or ''
    new_pass2 = request.form.get('password2') or ''

    # Проверки обязательных полей (логин и имя обязаны быть)
    if not new_login or not new_name:
        return render_template('lab4/edit.html', user_public={'login': new_login, 'name': new_name},
                               error='Логин и имя обязательны')

    for u in users:
        if u['login'] == new_login and u is not user:
            return render_template('lab4/edit.html', user_public={'login': new_login, 'name': new_name},
                                   error='Логин уже занят')

    # Обновляем логин и имя
    user['login'] = new_login
    user['name'] = new_name

   
    if new_pass or new_pass2:
        if new_pass != new_pass2:
            return render_template('lab4/edit.html', user_public={'login': new_login, 'name': new_name},
                                   error='Пароли не совпадают')
        user['password'] = new_pass

    session['user_name'] = new_name
    return redirect('/lab4/users')