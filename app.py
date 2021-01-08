from flask import Flask
#from datetime import datetime as dt
#import datetime
from functools import wraps
from flask_bcrypt import Bcrypt
from models import *

app = Flask(__name__)     

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/horas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql10385715:pWk1BJvenT@sql10.freemysqlhosting.net/sql10385715'
app.config['SECRET_KEY'] = "SuporteNP"

db.init_app(app)
bcrypt=Bcrypt(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)