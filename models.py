from settings import db, crypt
from datetime import datetime as dt

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100),nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True )
    password = db.Column(db.String(60), nullable=False)
    site = db.Column(db.String(15), nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime,index=False,nullable=False)
    updated_at = db.Column(db.DateTime,index=False,nullable=False)

    def __init__(self, name, login, email, password, site, level, active, created_at, updated_at):
        self.name = name
        self.login = login
        self.email = email
        self.password = crypt.generate_password_hash(password)
        self.site = site
        self.level = level
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

class registro_horas(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    login = db.Column(db.String(30),nullable=False)
    motivo = db.Column(db.String(100),nullable=False)
    aonde = db.Column(db.String(100),nullable=False)
    date = db.Column(db.Date,index=False,nullable=False)
    initial_time = db.Column(db.Time,index=False,nullable=False)
    pause_launch = db.Column(db.Time,index=False,nullable=False)
    back_launch = db.Column(db.Time,index=False,nullable=False)
    final_time = db.Column(db.Time,index=False,nullable=False)
    total_time = db.Column(db.Time,index=False,nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime,index=False,nullable=False)
    updated_at = db.Column(db.DateTime,index=False,nullable=False)

    def __init__(self, login, motivo, aonde, date, initial_time, pause_launch, back_launch, final_time, total_time, done, created_at, updated_at):
        self.login = login
        self.motivo = motivo
        self.aonde = aonde
        self.date = date
        self.initial_time = initial_time
        self.pause_launch = pause_launch
        self.back_launch = back_launch
        self.final_time = final_time
        self.total_time = total_time
        self.done = done
        self.created_at = created_at
        self.updated_at = updated_at

class sites(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    unidade = db.Column(db.String(30),nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime,index=False,nullable=False)

    def __init__(self, unidade, ativo, created_at):
        self.unidade = unidade
        self.ativo = True
        self.created_at = dt.now()