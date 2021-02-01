from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#ENV = 'dev'
#if ENV == 'dev':
#    app.debug = True
#    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql10385715:pWk1BJvenT@sql10.freemysqlhosting.net/sql10385715'
#else:
#    app.debug = False
#    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql10385715:pWk1BJvenT@sql10.freemysqlhosting.net/sql10385715'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://smoothz:tgo090393@horas.cgsqfhllrfsr.sa-east-1.rds.amazonaws.com/horas'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
app.config['SECRET_KEY'] = "SuporteNP"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

database = SQLAlchemy(app)
db = database

bcrypt = Bcrypt(app)
crypt = bcrypt