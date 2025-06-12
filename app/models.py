from datetime import datetime

from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    client_name = db.Column(db.String(100))
    direction = db.Column(db.String(10))  # "IN" or "OUT"
    item_name = db.Column(db.String(100))
    model = db.Column(db.String(100))
    collected_by = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)







