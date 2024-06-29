from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base
from config import SQLALCHEMY_DATABASE_URI

# Configuro el motor de base de datos y la cadena de conexion importando las constantes
# significativas para la app.
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()