from flask import Blueprint, url_for, redirect, request, abort, render_template
import datetime

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return 'ok'

@lab2.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Мария Юсупова', 2, 'ФБИ-34', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)

# ИЗМЕНИТЕ ИМЯ ФУНКЦИИ С lab2 НА lab (или другое имя)
@lab2.route('/lab2/')
def lab():  # ← ВАЖНО: измените имя функции!
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных... "
    return render_template('filter.html', phrase=phrase)

flower_list = [
    {'name': 'орхидея', 'price': 500},
    {'name': 'роза', 'price': 6000}
]

@lab2.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flowers=flower_list)

@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower_post():
    name = request.form.get('name', '').strip()
    price = request.form.get('price', '')
    
    if name and price:
        try:
            flower_list.append({  # ← ИСПРАВЛЕНО: было flower_list.lab2end
                'name': name, 
                'price': int(price)
            })
            return redirect('/lab2/flowers')
        except ValueError:
            return "Цена должна быть числом", 400
    return "Заполните все поля", 400

@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')

@lab2.route('/lab2/flowers/<int:flower_id>')
def show_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        return "Цветок не найден", 404
    return render_template('flower_detail.html', 
                         flower=flower_list[flower_id], 
                         flower_id=flower_id,
                         total=len(flower_list))

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'Сумма': a + b,
        'Разность': a - b,
        'Произведение': a * b,
        'Частное': a / b if b != 0 else 'Деление на ноль невозможно!',
        'Степень': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 350},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 283},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 416}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

dogs = [
    {'name': 'Лабрадор', 'image': 'labrador.jpg', 'description': 'Дружелюбная семейная собака, отличный пловец'},
    {'name': 'Немецкая овчарка', 'image': 'german_shepherd.jpg', 'description': 'Умная служебная порода, преданный защитник'},
    {'name': 'Такса', 'image': 'dachshund.jpg', 'description': 'Маленькая охотничья собака с длинным телом'},
    {'name': 'Бульдог', 'image': 'bulldog.jpg', 'description': 'Коренастая собака с характерной мордой'},
    {'name': 'Пудель', 'image': 'poodle.jpg', 'description': 'Умная порода с кудрявой шерстью, отличный компаньон'},
    {'name': 'Бигль', 'image': 'beagle.jpg', 'description': 'Охотничья собака с острым нюхом, очень активная'},
    {'name': 'Золотистый ретривер', 'image': 'golden_retriever.jpg', 'description': 'Добродушная собака с золотистой шерстью'},
    {'name': 'Сибирский хаски', 'image': 'husky.jpg', 'description': 'Ездовая собака с голубыми глазами, любит холод'},
    {'name': 'Доберман', 'image': 'doberman.jpg', 'description': 'Сильная и грациозная служебная порода'},
    {'name': 'Ротвейлер', 'image': 'rottweiler.jpg', 'description': 'Мощная собака с сильным защитным инстинктом'},
    {'name': 'Боксёр', 'image': 'boxer.jpg', 'description': 'Энергичная и игривая собака с выразительной мордой'},
    {'name': 'Джек-рассел-терьер', 'image': 'jack_russell.jpg', 'description': 'Маленькая, но очень активная и смелая собака'},
    {'name': 'Чихуахуа', 'image': 'chihuahua.jpg', 'description': 'Самая маленькая порода собак в мире'},
    {'name': 'Шпиц', 'image': 'spitz.jpg', 'description': 'Пушистая собака с лисьей мордочкой'},
    {'name': 'Мопс', 'image': 'pug.jpg', 'description': 'Маленькая собака с морщинистой мордой и курносым носом'},
    {'name': 'Колли', 'image': 'collie.jpg', 'description': 'Длинношерстная пастушья собака, известная по фильму "Лесси"'},
    {'name': 'Далматин', 'image': 'dalmatian.jpg', 'description': 'Собака с уникальным пятнистым окрасом'},
    {'name': 'Сенбернар', 'image': 'st_bernard.jpg', 'description': 'Крупная спасательная собака, очень добрая'},
    {'name': 'Шарпей', 'image': 'sharpei.jpg', 'description': 'Собака с многочисленными складками кожи'},
    {'name': 'Корги', 'image': 'corgi.jpg', 'description': 'Маленькая пастушья собака с короткими лапами'}
]

@lab2.route('/lab2/dogs')
def show_dogs():
    return render_template('dogs.html', dogs=dogs)