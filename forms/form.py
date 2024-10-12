from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField
from wtforms.validators import DataRequired


class GravitationForm(FlaskForm):
    m1 = FloatField("Масса первого объекта, кг", validators=[DataRequired()])
    m2 = FloatField("Масса второго объекта, кг", validators=[DataRequired()])
    r = FloatField("Расстояние, м", validators=[DataRequired()])
