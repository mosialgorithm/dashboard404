from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import PasswordField, StringField, EmailField, SelectField, SubmitField



class RegisterForm(FlaskForm):
    full_name = StringField('FullName', validators=[DataRequired(message='please enter your full name')])
    phone = StringField('PhoneNumber', validators=[DataRequired(message='please enter your phone number'), Length(min=11,max=11, message='please enter a valid phone number in Iran')])
    password = PasswordField('Password', validators=[DataRequired(message='please enter your password'), Length(min=8, message='please enter atleast 8 character')])
    password_confirm = PasswordField('PasswordConfirm', validators=[DataRequired(), EqualTo('password', message='please enter password confirm equal to password')])
     
    