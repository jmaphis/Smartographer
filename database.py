from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import sqlite3

current_app.config['SQLAlCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(current_app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    maps = db.relationship('Map', backref='user')

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    map_name = db.Column(db.String(30))
    map_type = db.Column(db.String(10), nullable=False)
    map_array = db.Column(db.String(4000), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Name %r>' %self.name