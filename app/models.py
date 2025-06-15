from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class StockItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    client_name = db.Column(db.String(100))
    project_name = db.Column(db.String(100))  # ✅ Required field
    collected_by = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    direction = db.Column(db.String(10))  # IN or OUT
    barcode = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
