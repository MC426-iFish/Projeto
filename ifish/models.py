from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))

    def __init__(self, name, email, password, userType):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = userType

class UserBuyer(User, db.Model, UserMixin):
    purchasesHistory = db.Column(db.String(100))
    def __init__(self, name, email, password, userType):
        super().__init__(name, email, password, userType)

class UserFisher(User, db.Model, UserMixin):
    stock = db.Column(db.String(100))
    def __init__(self, name, email, password, userType):
        super().__init__(name, email, password, userType)

        
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
