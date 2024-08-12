from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String,func,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import List,Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    fullname: Mapped[str] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(String(128))
    game_state: Mapped["GameState"] = relationship("GameState", uselist=False, back_populates="user")

    def set_password(self, password_to_hash):
        self.password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_hash):
        return check_password_hash(self.password, password_to_hash)


class GameState(Base):
    __tablename__ = 'game_states'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    chosen_case: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    current_round: Mapped[int] = mapped_column(Integer, default=0)
    playing: Mapped[bool] = mapped_column(Boolean, default=True)
    vals_left: Mapped[str] = mapped_column(String)
    revealed_cases: Mapped[str] = mapped_column(String)  
    offers: Mapped[Optional[str]] = mapped_column(String, nullable=True)  
    saved_at = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="game_state")
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