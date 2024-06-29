import os
from dotenv import load_dotenv
# Cargar el archivo .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
# Configuro el motor de base de datos y la cadena de conxion
# Con SQite
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'base.db')

# Con MySQL, debemos tenes instalado pymysql

# Basicos
# HOST='SU_HOST' 
# USER='SU_USER'
# PWDS='SU_PASSWORD'
# DBA='SU_BASE_DE_DATOS'
# PORT='SU_PUERTO'

# Ejemplo:
# HOST='192.168.0.10' 
# USER='root'
# PWDS='Dany5170#'
# DBA='sampledbpy'
# PORT='3306'
# STRCNX=f'mysql+pymysql://{USER}:{PWDS}@{HOST}:{PORT}/{DBA}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True if os.environ.get('ENVIROMENT') == 'local' else False
PORT = int(os.environ.get('PORT', 5000))
## ---------------------------------------------------------------------------

var_globales= {
    'title': 'Mi App de Flask',
    'mensaje': ''
}
