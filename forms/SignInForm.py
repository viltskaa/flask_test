from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, EmailField
from wtforms.validators import DataRequired, Email


# pip install email-validator

class SignInForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])