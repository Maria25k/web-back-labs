from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user

lab9 = Blueprint('lab9', __name__, template_folder='templates')

# Списки поздравлений и подарков
congratulations = [
    "С Новым Годом! Пусть в наступающем году сбудутся все ваши мечты!",
    "Желаю счастья, здоровья и успехов в новом году!",
    "Пусть новый год принесет много радости и тепла в ваш дом!",
    "Желаю, чтобы каждый день нового года был наполнен улыбками!",
    "Пусть все плохое останется в старом году, а в новом будут только хорошие новости!",
    "Желаю финансового благополучия и карьерного роста в новом году!",
    "Пусть новый год будет полон интересных путешествий и открытий!",
    "Желаю крепкого здоровья вам и вашим близким!",
    "Пусть в новом году исполнятся все ваши самые заветные желания!",
    "Желаю любви, тепла и уюта в новом году!",
    "Пусть новый год принесет много приятных сюрпризов!",
    "Желаю творческих успехов и вдохновения!",
    "Пусть в вашем доме всегда царит гармония и счастье!",
    "Желаю новых интересных знакомств и встреч!",
    "Пусть каждый день нового года будет лучше предыдущего!"
]

# Символы подарков (эмодзи)
gifts = ["🎁", "🎄", "⭐", "❄️", "🎅", "🤶", "🦌", "🔔", "🕯️", "🍪"]

total_boxes = 20  # Всего коробок

@lab9.route('/')
def main():
    # Инициализируем сессию для хранения открытых пользователем коробок
    if 'opened_by_user' not in session:
        session['opened_by_user'] = []
    
    # Генерируем начальное состояние коробок
    if 'boxes_state' not in session:
        session['boxes_state'] = {}
        for i in range(total_boxes):
            session['boxes_state'][str(i)] = {
                'opened': False,
                'congratulation': congratulations[i % len(congratulations)],
                'gift': gifts[i % len(gifts)]
            }
    
    # Считаем статистику
    user_opened_count = len(session.get('opened_by_user', []))
    remaining = 3 - user_opened_count
    
    return render_template('lab9/index.html', 
                         total_boxes=total_boxes,
                         opened_count=user_opened_count,
                         remaining=remaining,
                         is_authenticated=current_user.is_authenticated)

@lab9.route('/api/get_boxes')
def get_boxes():
    # Возвращаем состояние всех коробок
    boxes_data = []
    boxes_state = session.get('boxes_state', {})
    
    for i in range(total_boxes):
        box_state = boxes_state.get(str(i), {'opened': False})
        boxes_data.append({
            'id': i,
            'opened': box_state['opened']
        })
    
    # Подсчитываем количество открытых коробок пользователем
    user_opened_count = len(session.get('opened_by_user', []))
    
    return jsonify({
        'boxes': boxes_data,
        'total_opened': user_opened_count,
        'remaining': 3 - user_opened_count,
        'total_boxes': total_boxes,
        'is_authenticated': current_user.is_authenticated
    })

@lab9.route('/api/open_box', methods=['POST'])
def open_box():
    try:
        box_id = request.json.get('box_id')
        
        if box_id is None or int(box_id) >= total_boxes:
            return jsonify({'error': 'Неверный номер коробки'}), 400
        
        box_id_str = str(box_id)
        
        # Инициализируем сессии если их нет
        if 'boxes_state' not in session:
            session['boxes_state'] = {}
        if 'opened_by_user' not in session:
            session['opened_by_user'] = []
        
        # Проверяем, открывал ли пользователь эту коробку
        if int(box_id) in session.get('opened_by_user', []):
            return jsonify({'error': 'Эта коробка уже открыта вами'}), 400
        
        # Проверяем лимит коробок (максимум 3)
        if len(session.get('opened_by_user', [])) >= 3:
            return jsonify({'error': 'Вы уже открыли максимальное количество коробок (3)'}), 400
        
        # Проверяем, открыта ли коробка (глобально)
        box_state = session['boxes_state'].get(box_id_str, {'opened': False})
        if box_state.get('opened', False):
            return jsonify({'error': 'Эта коробка уже пуста'}), 400
        
        # Для некоторых коробок требуем авторизацию
        if int(box_id) in [5, 10, 15] and not current_user.is_authenticated:
            return jsonify({'error': 'Эта коробка доступна только авторизованным пользователям'}), 403
        
        # Открываем коробку
        if box_id_str not in session['boxes_state']:
            session['boxes_state'][box_id_str] = {
                'opened': True,
                'congratulation': congratulations[int(box_id) % len(congratulations)],
                'gift': gifts[int(box_id) % len(gifts)]
            }
        else:
            session['boxes_state'][box_id_str]['opened'] = True
        
        # Добавляем в список открытых пользователем
        if int(box_id) not in session['opened_by_user']:
            session['opened_by_user'].append(int(box_id))
        
        session.modified = True
        
        return jsonify({
            'success': True,
            'congratulation': session['boxes_state'][box_id_str]['congratulation'],
            'gift': session['boxes_state'][box_id_str]['gift'],
            'opened_count': len(session['opened_by_user']),
            'remaining': 3 - len(session['opened_by_user'])
        })
    
    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500

@lab9.route('/api/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    try:
        # Сброс всех коробок (только для авторизованных пользователей)
        session['boxes_state'] = {}
        for i in range(total_boxes):
            session['boxes_state'][str(i)] = {
                'opened': False,
                'congratulation': congratulations[i % len(congratulations)],
                'gift': gifts[i % len(gifts)]
            }
        
        # Очищаем список открытых пользователем коробок
        session['opened_by_user'] = []
        
        session.modified = True
        
        return jsonify({'success': True, 'message': 'Все коробки снова наполнены!'})
    
    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500

@lab9.route('/api/get_box_content/<int:box_id>')
def get_box_content(box_id):
    if box_id >= total_boxes:
        return jsonify({'error': 'Неверный номер коробки'}), 400
    
    boxes_state = session.get('boxes_state', {})
    box_state = boxes_state.get(str(box_id), {})
    
    if not box_state:
        # Если коробка еще не инициализирована, создаем данные
        box_state = {
            'congratulation': congratulations[box_id % len(congratulations)],
            'gift': gifts[box_id % len(gifts)]
        }
    
    return jsonify({
        'congratulation': box_state.get('congratulation', congratulations[box_id % len(congratulations)]),
        'gift': box_state.get('gift', gifts[box_id % len(gifts)])
    })
