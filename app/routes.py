# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Questions, Answers, TestAnswers
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, IndexForm, LoginForm

import pandas as pd
import random


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first()
    otdel = user.otdel
    tests = TestAnswers.query.filter_by(username=current_user.username)
    form = IndexForm()
    if form.validate_on_submit():
        return redirect(url_for('test'))

    return render_template(
            'index.html', title='Home', tests=tests, otdel=otdel, form=form)


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
    return render_template('login.html', title='Начать тестирование', form=form)


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
        user = User(username=form.username.data, otdel=form.otdel.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрированы, войдите по зарегистрированному имени.')

        otdel = form.otdel.data
        df_1 = pd.read_csv('./data/data.csv')
        df_2 = pd.read_csv('./data/ans.csv')

        dep_type = {
            'ОПиР': {'python': 6, 'ds': 6, 'c#': 0, 'sql': 3},
            'ОАКБ': {'python': 5, 'ds': 5, 'c#': 0, 'sql': 5},
            'ОАРБ': {'python': 5, 'ds': 0, 'c#': 0, 'sql': 10},
            'ОАРБ_c#': {'python': 4, 'ds': 0, 'c#': 3, 'sql': 8},
            'ОАОП': {'python': 10, 'ds': 2, 'c#': 0, 'sql': 3},
            'ОАОП_c#': {'python': 5, 'ds': 0, 'c#': 5, 'sql': 5},
            'ОАКБ_python': {'python': 15, 'ds': 0, 'c#': 0, 'sql': 0},
            'ОАОП_sql': {'python': 0, 'ds': 0, 'c#': 0, 'sql': 15},
            'ОАРБ_sql': {'python': 0, 'ds': 0, 'c#': 0, 'sql': 15},
        }
        python_q = df_1.iloc[random.sample(range(0, 15), dep_type[otdel]['python']), 0:2]
        ds_q = df_1.iloc[random.sample(range(16, 25), dep_type[otdel]['ds']), 0:2]
        c_q = df_1.iloc[random.sample(range(26, 32), dep_type[otdel]['c#']), 0:2]
        sql_q = df_1.iloc[random.sample(range(33, 48), dep_type[otdel]['sql']), 0:2]
        all_data = [python_q, ds_q, c_q, sql_q]
        tests = []
        userdata = []
        num = 1
        for data in all_data:
            for i in range(data.shape[0]):
                ques = []
                tests.append({'questions': '', 'answers': ''})
                ques.append('Вопрос ' + str(num) + ':')
                ques.append(str(data.iloc[i]['question']))
                tests[num-1]['questions'] = ques

                userdata.append({'user': '', 'questions': '', 'answers': ''})
                userdata[num-1]['questions'] = str(data.iloc[i]['question'])
                userdata[num-1]['user'] = user
                ans = df_2[df_2['question_id'] == data.iloc[i]['id']]
                answ = []
                useransw = ''
                for j in range(ans.shape[0]):
                    answ.append(str(ans.iloc[j]['answer']))
                    if ans.iloc[j]['yes_no'] == 1:
                        useransw = ans.iloc[j]['answer']
                tests[num-1]['answers'] = answ
                userdata[num-1]['answers'] = useransw
                num += 1
                testdata = TestAnswers(username=str(user),
                                       question=str(data.iloc[i]['question']),
                                       answer=str(useransw))
                db.session.add(testdata)
                db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/test')
@login_required
def test():
    return render_template('test.html', title='Итоги тестирования')
