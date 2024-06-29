from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.cli import FlaskGroup
import config

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.models import * 

def create_app():
    return app

cli = FlaskGroup(create_app=create_app)

if __name__ == '__main__':
    cli()