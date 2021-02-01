from flask import Flask
import models
from settings import app, db, crypt

from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
