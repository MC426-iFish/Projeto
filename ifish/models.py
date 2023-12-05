from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     notes = db.relationship('Note')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # fishInventory = db.relationship('FishInventory')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

# class FishInventory():
#     id = db.Column(db.Integer, primary_key=True)
#     type = db.Column(db.String(100))
#     fishDate = db.Column(db.String(100))
#     quantity = db.Column(db.Integer)
#     price = db.Column(db.Integer)
    
#     def __init__(self, type, fishDate, quantity, price):
#         self.type = type
#         self.fishDate = fishDate
#         self.quantity = quantity
#         self.price = price
