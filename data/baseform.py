from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    select = SelectField('Все', validators=[DataRequired()], choices=[("Все", "Все"), ("Телефоны", "Телефоны"), ("ПК", "ПК")])
    search = StringField('Поиск', validators=[DataRequired()])
    submit = SubmitField('Поиск')
