from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint('main', __name__, template_folder="templates", static_folder="static")

@main_bp.route('/')
@main_bp.route('/home')
def index():
    return render_template('index.html')
