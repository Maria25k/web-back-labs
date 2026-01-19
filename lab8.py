from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from os import path
from db import db
from db.models import users, articles
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__)

# Настройка соединения с БД будет в app.py

# Регистрация
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    # Проверка на пустые значения
    if not login_form or not password_form:
        return render_template('lab8/register.html', 
                             error='Логин и пароль не могут быть пустыми')
    
    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                             error='Такой пользователь уже существует')
    
    # Создание нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический логин после регистрации
    login_user(new_user, remember=False)
    
    return redirect('/lab8/')

# Авторизация
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember') == 'on'
    
    # Проверка на пустые значения
    if not login_form or not password_form:
        return render_template('lab8/login.html', 
                             error='Логин и пароль не могут быть пустыми')
    
    # Поиск пользователя в БД
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        return redirect(next_page or '/lab8/')
    
    return render_template('lab8/login.html', 
                         error='Ошибка входа: неверный логин или пароль')

# Логаут
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# Главная страница lab8
@lab8.route('/lab8/')
def index():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/index.html', username=username)

# Список статей
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    # Получаем статьи текущего пользователя
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    # Получаем публичные статьи других пользователей
    public_articles = articles.query.filter(
        articles.is_public == True, 
        articles.login_id != current_user.id
    ).all()
    return render_template('lab8/articles.html', 
                         user_articles=user_articles,
                         public_articles=public_articles)

# Создание статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create.html', 
                             error='Заголовок и текст статьи не могут быть пустыми')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit.html', 
                             article=article,
                             error='Заголовок и текст статьи не могут быть пустыми')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    return redirect('/lab8/articles/')

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if article:
        db.session.delete(article)
        db.session.commit()
    
    return redirect('/lab8/articles/')

# Поиск статей
@lab8.route('/lab8/search')
@login_required
def search_articles():
    query = request.args.get('q', '')
    
    if not query:
        return redirect('/lab8/articles/')
    
    # Поиск в своих статьях и публичных статьях
    search_results = articles.query.filter(
        or_(
            articles.login_id == current_user.id,
            articles.is_public == True
        ),
        or_(
            articles.title.ilike(f'%{query}%'),
            articles.article_text.ilike(f'%{query}%')
        )
    ).all()
    
    return render_template('lab8/search.html', 
                         query=query,
                         results=search_results)