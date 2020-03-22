# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, IndexForm, LoginForm
import time
from app.testmaker import make_test
from app.makeresult import make_result


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first()
    otdel = user.otdel
    seed = user.seed
    _, tests, _ = make_test(user, otdel, seed)
    form = IndexForm()
    if request.method == 'POST':
        return redirect(url_for('test'))
    return render_template(
            'index.html', title='Home', otdel=otdel, tests=tests, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Выбирите другое имя!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template(
            'login.html', title='Начать тестирование', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
                username=form.username.data,
                otdel=form.otdel.data, seed=int(time.time()))
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрированы, войдите по зарегистрированному имени.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    user = User.query.filter_by(username=current_user.username).first()
    if len(request.form) != 16:
        flash('Необходимо ответить на все вопросы!')
        return redirect(url_for('index'))
    userdata, _, dep_type = make_test(user.username, user.otdel, user.seed)
    dep_type, result, result_part, pos_result, all_result, part_pos_result = make_result(
        request.form, userdata, dep_type, user.otdel)

    return render_template(
            'test.html', user=current_user.username,
            otdel=user.otdel,
            dep_type=dep_type,
            result=result,
            result_part=result_part,
            pos_result=pos_result,
            all_result=all_result,
            part_pos_result=part_pos_result,
            title='Итоги тестирования')
