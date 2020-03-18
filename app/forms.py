from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError
from app.models import User
#from flask_login import current_user
import pickle

otdels = [
        {'label': 'ОПиР', 'value': 'ОПиР'},
        {'label': 'ОАКБ', 'value': 'ОАКБ'},
        {'label': 'ОАРБ', 'value': 'ОАРБ'},
        {'label': 'ОАРБ_c#', 'value': 'ОАРБ_c#'},
        {'label': 'ОАОП', 'value': 'ОАОП'},
        {'label': 'ОАОП_c#', 'value': 'ОАОП_c#'},
        {'label': 'ОАКБ_python', 'value': 'ОАКБ_python'},
        {'label': 'ОАОП_sql', 'value': 'ОАОП_sql'},
        {'label': 'ОАРБ_sql', 'value': 'ОАРБ_sql'},
        ]

with open('test4.pkl', 'rb') as f:
    datatests = pickle.load(f)


class LoginForm(FlaskForm):
    username = StringField('ФИО Тестируемого', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Продолжить')

class RegistrationForm(FlaskForm):
    username = StringField('ФИО Тестируемого', validators=[DataRequired()])
    otdel = SelectField('Выбирите отдел', default = '', validators=[DataRequired()],
                    choices=[(otdel['label'], otdel['value']) for otdel in otdels])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Выбирите другое имя.')

class IndexForm(FlaskForm):
    testdata = []
    for i in datatests:
        tests = RadioField(label = i['questions'][0]+'\n'+i['questions'][1], 
                              validators=[DataRequired()],
            choices=[(answer, answer) for answer in i['answers']])
        testdata.append(tests)
    submit = SubmitField('Отправить ответы')
