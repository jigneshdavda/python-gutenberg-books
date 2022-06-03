from flask import Flask
import config
from flask_mysqldb import MySQL
from flask_sieve import Sieve

# Init the Flask module
app = Flask(__name__)

# app configurations
app.config['MYSQL_HOST'] = config.DB_HOST
app.config['MYSQL_USER'] = config.DB_USER
app.config['MYSQL_PASSWORD'] = config.DB_PASSWORD
app.config['MYSQL_DB'] = config.DB_NAME
app.config['MYSQL_CURSORCLASS'] = config.DB_CURSORCLASS
app.config['SECRET_KEY'] = config.SECRET_KEY

# Init MySQL module
mysql = MySQL(app)

# Init Sieve module for form validations
Sieve(app)

# Register Admin APIs
from app.routes.api import guternberg_api
app.register_blueprint(guternberg_api)