from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from werkzeug.exceptions import BadRequest, NotFound
from models.models import User
import db


app = Flask(__name__)
app.config.from_object('config')


login_manager = LoginManager(app)
login_manager.login_view = 'auth.login' 
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('unauthorized.html')


from auth.routes import auth_bp
from main.routes import main_bp
from users.routes import users_bp

app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')

from config import var_globales
@app.context_processor
def inject_variables():
    return var_globales


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=app.config["DEBUG"])
