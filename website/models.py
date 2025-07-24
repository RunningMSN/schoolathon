from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    fruit_password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    team = db.Column(db.String(150))

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    region = db.Column(db.String(150))
    state = db.Column(db.String(150))
    name = db.Column(db.String(150))
    community_college = db.Column(db.Boolean)
    hbcu = db.Column(db.Boolean)
    msi = db.Column(db.Boolean)
    advisors = db.Column(db.Boolean)
    completed = db.Column(db.Boolean, default=False)