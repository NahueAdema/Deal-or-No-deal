from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from models.models import User
from db import session
from config import var_globales

users_bp = Blueprint (
    "users_bp", __name__, template_folder="templates", static_folder="static"
)


@users_bp.route('/')
@login_required
def users():
    
    users = session.query(User).all()
    return render_template('users/items.html', users=users)


@users_bp.route('/<int:user_id>')
@login_required
def getuser(user_id):
    
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        var_globales['mensaje'] = 'NO EXISTE EL USUARIO'
    return render_template('users/item.html', user=user) 


@users_bp.route('/delete/<int:user_id>')
@login_required
def deleteuser(user_id:int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        try:
            session.delete(user)
            session.commit()
        except Exception as e:
            print(f'Error al eliminar. {e}')
    return redirect('/users')



@users_bp.route('/edit/<int:user_id>', methods=["GET", "POST"])
@login_required
def edituser(user_id:int):
    
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if request.method == 'POST':
            
            name = request.form['username']
            password = request.form['password']
            
            user.name = name
            user.password = password
            try:
                
                session.commit()
            except Exception as e:
                print(f'A courrido un error {e}')
            return redirect('/users')
        else:
            return render_template('users/edit.html', user=user)







