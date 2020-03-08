from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

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


class LoginForm(FlaskForm):
    username = StringField('Тестируемый, ФИО', validators=[DataRequired()])
    # password = PasswordField('Отдел', validators=[DataRequired()])
    otdel = SelectField('Отдел', default = '', validators=[DataRequired()],
                    choices=[(otdel['label'], otdel['value']) for otdel in otdels])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Продолжить')
