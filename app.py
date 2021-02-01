from flask import Flask
import models
from settings import app, db, crypt

from routes import *

if __name__ == "__main__":
    app.run()