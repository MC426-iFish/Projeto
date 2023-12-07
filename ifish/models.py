from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    purchasesHistory = db.Column(db.String(100))
    fishInventory = db.relationship('Fish', backref='owner', lazy=True)

    def __init__(self, name, email, password, userType):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = userType

    def add_fish(self, type, fishDate, quantity, price):
        pass

class UserBuyer(User, db.Model, UserMixin):
    
    def __init__(self, name, email, password, userType):
        super().__init__(name, email, password, userType)
       

class UserFisher(User, db.Model, UserMixin):
    
    def __init__(self, name, email, password, userType):
        super().__init__(name, email, password, userType)

    def add_fish(self, type, fishDate, quantity, price):
        new_fish = Fish(type=type, fishDate=fishDate, quantity=quantity, price=price)
        self.fishInventory.append(new_fish)
        db.session.add(new_fish)
        db.session.commit()


class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    fishDate = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, type, fishDate, quantity, price):
        self.type = type
        self.fishDate = fishDate
        self.quantity = quantity
        self.price = price


