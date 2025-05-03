from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note')