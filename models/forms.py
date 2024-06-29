from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='Por favor, introduce tu nombre de usuario.'),
        Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 caracteres.')
    ])
    fullname = StringField('Nombre Completo del usuario', validators=[
        DataRequired(message='Por favor, introduce su nombre completo.'),
        Length(min=1, max=80, message='El nombre de usuario debe tener entre 1 y 80 caracteres.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Por favor, introduce tu contraseña.'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
    ])
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message='Por favor, confirma tu contraseña.'),
        EqualTo('password', message='Las contraseñas deben coincidir.')
    ])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(message='Por favor, introduce tu nombre de usuario.')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Por favor, introduce tu contraseña.')])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')