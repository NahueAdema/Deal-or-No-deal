from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String,func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import List,Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Clase que me permite interactuar con la Base de Datos
Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25))
    fullname: Mapped[str] = mapped_column(String(80))
    password : Mapped[str] = mapped_column(String(128))
    
    def set_password(self, password_to_hash):
        self.password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_hash):
        return check_password_hash(self.password, password_to_hash)
    
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='Por favor, introduce tu nombre de usuario.'),
        Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 caracteres.')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='Por favor, introduce tu contraseña.')
    ])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

# Clase para Registracion de User
class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(message='Por favor, introduce tu nombre de usuario.'),
        Length(min=4, max=25, message='El nombre de usuario debe tener entre 4 y 25 caracteres.')
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