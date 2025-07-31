from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()
class User(UserMixin, db.Model):
id       = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(80), unique=True, nullable=False)
password = db.Column(db.String(255), nullable=False)
class Video(db.Model):
id          = db.Column(db.Integer, primary_key=True)
owner_id    = db.Column(db.Integer, db.ForeignKey('user.id'))
title       = db.Column(db.String(120), nullable=False)
description = db.Column(db.Text)
filename    = db.Column(db.String(255), nullable=False)
s3_key      = db.Column(db.String(255))
created_at  = db.Column(db.DateTime, default=datetime.utcnow)
status      = db.Column(db.String(20), default='uploaded')
thumbnail   = db.Column(db.String(255))
owner = db.relationship('User', backref='videos')
