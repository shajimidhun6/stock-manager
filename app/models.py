from datetime import datetime

from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # <== New
    item_name = db.Column(db.String(120), nullable=False)  # <== Updated
    model = db.Column(db.String(120))  # <== New
    collected_by = db.Column(db.String(120))
    quantity = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime)






