from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    search = StringField(validators=[DataRequired()])
