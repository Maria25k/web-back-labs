from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab33():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')

    if not name:
        name = 'Аноним'
    if not age:
        age = 'неизвестен'

    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'blue')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    if sex == '':
        errors['sex'] = 'Заполните поле!'
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    drink = request.args.get('drink')
    milk = request.args.get('milk')
    sugar = request.args.get('sugar')
    
    price = 0
    
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    elif drink == 'green-tea':
        price = 70
    
    if milk == 'on':
        price += 30
    if sugar == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price') or "0"
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    bold = request.args.get('bold')
    
    if color or bg_color or font_size or bold:
        resp = make_response(redirect('/lab3/settings'))
        
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if bold:
            resp.set_cookie('bold', bold)
        else:
            resp.delete_cookie('bold')  
        return resp
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    bold = request.cookies.get('bold')
    
    return render_template('lab3/settings.html', 
                         color=color, 
                         bg_color=bg_color, 
                         font_size=font_size, 
                         bold=bold)

@lab3.route('/lab3/settings_reset')
def settings_reset():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('bold')
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    # Валидация
    if fio is not None:
        if fio.strip() == '':
            errors['fio'] = 'Заполните ФИО'
    
    if age is not None:
        if age.strip() == '':
            errors['age'] = 'Заполните возраст'
        else:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 120:
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом'
    
    if departure is not None and departure.strip() == '':
        errors['departure'] = 'Заполните пункт выезда'
    
    if destination is not None and destination.strip() == '':
        errors['destination'] = 'Заполните пункт назначения'
    
    if date is not None and date.strip() == '':
        errors['date'] = 'Выберите дату'
    
    # Расчет стоимости
    price = 0
    if not errors and fio:
        # Базовая стоимость
        if age and int(age) < 18:
            price = 700  # Детский
        else:
            price = 1000  # Взрослый
        
        # Доплата за полку
        if shelf in ['lower', 'lower-side']:
            price += 100
        
        # Доплаты
        if linen == 'on':
            price += 75
        if luggage == 'on':
            price += 250
        if insurance == 'on':
            price += 150
    
    # Если есть ошибки или форма не отправлена
    if errors or not request.args:
        return render_template('lab3/ticket.html',
                             fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                             age=age, departure=departure, destination=destination,
                             date=date, insurance=insurance, errors=errors)
    
    # Если все OK - показываем билет
    return render_template('lab3/ticket.html',
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, price=price)


products = [
    {'name': 'iPhone 15', 'price': 89990, 'brand': 'Apple', 'color': 'черный'},
    {'name': 'Samsung Galaxy S24', 'price': 79990, 'brand': 'Samsung', 'color': 'белый'},
    {'name': 'Xiaomi 14', 'price': 59990, 'brand': 'Xiaomi', 'color': 'синий'},
    {'name': 'Google Pixel 8', 'price': 69990, 'brand': 'Google', 'color': 'серый'},
    {'name': 'OnePlus 11', 'price': 54990, 'brand': 'OnePlus', 'color': 'зеленый'},
    {'name': 'Sony Xperia 5 V', 'price': 89990, 'brand': 'Sony', 'color': 'черный'},
    {'name': 'Nothing Phone 2', 'price': 44990, 'brand': 'Nothing', 'color': 'белый'},
    {'name': 'Realme GT 3', 'price': 39990, 'brand': 'Realme', 'color': 'желтый'},
    {'name': 'Honor Magic 5', 'price': 64990, 'brand': 'Honor', 'color': 'синий'},
    {'name': 'iPhone 14', 'price': 69990, 'brand': 'Apple', 'color': 'фиолетовый'},
    {'name': 'Samsung Galaxy A54', 'price': 29990, 'brand': 'Samsung', 'color': 'черный'},
    {'name': 'Xiaomi Redmi Note 13', 'price': 19990, 'brand': 'Xiaomi', 'color': 'белый'},
    {'name': 'Google Pixel 7a', 'price': 39990, 'brand': 'Google', 'color': 'зеленый'},
    {'name': 'Nokia G42', 'price': 17990, 'brand': 'Nokia', 'color': 'фиолетовый'},
    {'name': 'Motorola Edge 40', 'price': 34990, 'brand': 'Motorola', 'color': 'синий'},
    {'name': 'Asus Zenfone 10', 'price': 59990, 'brand': 'Asus', 'color': 'черный'},
    {'name': 'iPhone SE 2022', 'price': 44990, 'brand': 'Apple', 'color': 'красный'},
    {'name': 'Samsung Galaxy Z Flip5', 'price': 99990, 'brand': 'Samsung', 'color': 'фиолетовый'},
    {'name': 'Xiaomi 13T', 'price': 49990, 'brand': 'Xiaomi', 'color': 'черный'},
    {'name': 'OnePlus Nord 3', 'price': 34990, 'brand': 'OnePlus', 'color': 'зеленый'},
    {'name': 'iPhone 13 mini', 'price': 59990, 'brand': 'Apple', 'color': 'синий'},
    {'name': 'Samsung Galaxy S23 FE', 'price': 54990, 'brand': 'Samsung', 'color': 'белый'},
    {'name': 'Google Pixel 6a', 'price': 29990, 'brand': 'Google', 'color': 'черный'},
    {'name': 'Xiaomi Poco F5', 'price': 29990, 'brand': 'Xiaomi', 'color': 'синий'},
    {'name': 'Nothing Phone 1', 'price': 29990, 'brand': 'Nothing', 'color': 'белый'}
]

@lab3.route('/lab3/products')
def products_search():
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    action = request.args.get('action')  
    
    if action == 'reset':
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    if min_price is not None or max_price is not None:
        resp = make_response(redirect('/lab3/products'))
        if min_price:
            resp.set_cookie('min_price', min_price)
        else:
            resp.delete_cookie('min_price')
        
        if max_price:
            resp.set_cookie('max_price', max_price)
        else:
            resp.delete_cookie('max_price')
        
        return resp
    
    min_price = request.cookies.get('min_price')
    max_price = request.cookies.get('max_price')
    
    min_price_int = None
    max_price_int = None
    
    if min_price:
        try:
            min_price_int = int(min_price)
        except ValueError:
            min_price_int = None
    
    if max_price:
        try:
            max_price_int = int(max_price)
        except ValueError:
            max_price_int = None
    
    filtered_products = []
    
    if min_price_int is not None or max_price_int is not None:
        for product in products:
            price = product['price']
            
            if min_price_int is not None and price < min_price_int:
                continue
            
            if max_price_int is not None and price > max_price_int:
                continue
            
            filtered_products.append(product)
    else:
        filtered_products = products.copy()
    
    if min_price_int is not None and max_price_int is not None and min_price_int > max_price_int:
        min_price_int, max_price_int = max_price_int, min_price_int
        min_price, max_price = max_price, min_price
    
    all_prices = [p['price'] for p in products]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    return render_template('lab3/products.html',
                         products=filtered_products,
                         min_price=min_price,
                         max_price=max_price,
                         global_min_price=global_min_price,
                         global_max_price=global_max_price,
                         count=len(filtered_products),
                         total=len(products))