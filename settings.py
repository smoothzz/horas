from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

#ENV = 'dev'
#if ENV == 'dev':
#    app.debug = True
#    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
#else:
#    app.debug = False
def con_try():
	try:
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://smoothz:password@localhost/horas'
	except:
		return "<h1>Cannot connect to DB</h1>"	
con_try()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
app.config['SECRET_KEY'] = "suporte"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

database = SQLAlchemy(app)
db = database

bcrypt = Bcrypt(app)
crypt = bcrypt
