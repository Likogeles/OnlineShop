from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class AddProductForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    number = StringField('Количество', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    # image = SubmitField('Зарегестрироваться')
    submit = SubmitField('Добавить')
