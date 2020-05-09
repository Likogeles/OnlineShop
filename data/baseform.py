from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    select = SelectField('Все', validators=[DataRequired()])
    search = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
