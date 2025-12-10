from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab44():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['GET', 'POST'])
def div():
    if request.method == 'GET':
        return render_template('lab4/div.html')

    # Если POST — обрабатываем данные
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Проверка на пустые значения
    if not x1 or not x2:
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    # Преобразование в числа с обработкой ошибок
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Введите корректные числа!')

    # Проверка на деление на ноль
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum():
    if request.method == 'GET':
        return render_template('lab4/sum.html')

    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sum.html', error='Введите корректные числа!')

    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul', methods=['GET', 'POST'])
def mul():
    if request.method == 'GET':
        return render_template('lab4/mul.html')

    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/mul.html', error='Введите корректные числа!')

    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub', methods=['GET', 'POST'])
def sub():
    if request.method == 'GET':
        return render_template('lab4/sub.html')

    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if not x1 or not x2:
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Введите корректные числа!')

    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow', methods=['GET', 'POST'])
def pow_view():
    if request.method == 'GET':
        return render_template('lab4/pow.html')

    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    # Ошибка при пустых полях
    if not x1 or not x2:
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    try:
        a = float(x1)
        b = float(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Введите корректные числа!')

    # Явная проверка 0^0 — до вычисления, чтобы не полагаться на поведение Python
    if a == 0 and b == 0:
        return render_template('lab4/pow.html', error='0^0 — неопределённость!')

    try:
        result = a ** b
    except OverflowError:
        return render_template('lab4/pow.html', error='Результат слишком большой!')
    except Exception as e:
        return render_template('lab4/pow.html', error=f'Ошибка при вычислении: {e}')

    return render_template('lab4/pow.html', x1=a, x2=b, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
  
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'm'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Петров', 'gender': 'm'},
    {'login': 'sur', 'password': '999', 'name': 'Сергей Юрьев', 'gender': 'm'},
    {'login': 'alena', 'password': '2105', 'name': 'Алёна Квашнина', 'gender': 'f'},
    {'login': 'nik', 'password': '2121', 'name': 'Николай Смирнов', 'gender': 'm'}
]


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
    if request.method == 'GET':
        return render_template('lab4/fridge.html')

    temp = request.form.get('temperature')

    # Если температура не введена
    if temp is None or temp == '':
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')

    try:
        temp = int(temp)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите число')

    # Проверки диапазонов
    if temp < -12:
        return render_template('lab4/fridge.html',
                               error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html',
                               error='Не удалось установить температуру — слишком высокое значение')


    if -12 <= temp <= -9:
        snowflakes = "❄❄❄"
    elif -8 <= temp <= -5:
        snowflakes = "❄❄"
    else:  # -4 ... -1
        snowflakes = "❄"

    return render_template('lab4/fridge.html',
                           temperature=temp,
                           snowflakes=snowflakes)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    prices = {
        'ячмень': 12000,
        'овёс': 8500,
        'пшеница': 9000,
        'рожь': 15000
    }

    if request.method == 'GET':
        return render_template('lab4/grain.html', prices=prices)

    grain_type = request.form.get('grain')
    weight = request.form.get('weight')

    # Проверка веса
    if not weight:
        return render_template('lab4/grain.html', error="Ошибка: вес не указан!", prices=prices)

    try:
        weight = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error="Ошибка: введите число!", prices=prices)

    if weight <= 0:
        return render_template('lab4/grain.html', error="Ошибка: вес должен быть больше 0!", prices=prices)

    if weight > 100:
        return render_template('lab4/grain.html', error="Такого объёма сейчас нет в наличии!", prices=prices)

    price_per_ton = prices.get(grain_type)
    total = price_per_ton * weight

    discount = 0
    discount_text = None

    if weight > 10:
        discount = total * 0.10
        total = total - discount
        discount_text = f"Применена скидка 10% за большой объём. Скидка: {discount:.2f} руб."

    return render_template(
        'lab4/grain.html',
        grain_type=grain_type,
        weight=weight,
        total=total,
        discount_text=discount_text,
        prices=prices
    )


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