from flask import Flask
#from datetime import datetime as dt
#import datetime
from functools import wraps
from flask_bcrypt import Bcrypt
from models import *

app = Flask(__name__)     

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://adznetsqkutjcl:bcdd79f82b7945b6aff2eaa71c414aa913d44f73028e59aced99f1b95ca8e95b@ec2-50-19-32-202.compute-1.amazonaws.com:5432/d3nu4cp25ctfb8'

app.config['SECRET_KEY'] = "SuporteNP"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt=Bcrypt(app)

from routes import *

if __name__ == "__main__":
    app.run()
    #app.run(debug=True)