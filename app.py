from flask import Flask
from functools import wraps
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import users, registro_horas, sites

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql10385715:pWk1BJvenT@sql10.freemysqlhosting.net/sql10385715'

app.config['SECRET_KEY'] = "SuporteNP"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bcrypt=Bcrypt(app)

from routes import *

if __name__ == "__main__":
    app.run()