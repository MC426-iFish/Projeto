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

    def search_fish(self, fish_type):
        if fish_type in [i.type for i in self.fishInventory]:
            return Fish.query.filter_by(type=fish_type).filter_by(user_id=self.id).first()
        return None
            
    def add_fish(self, type, fishDate, quantity, price):
        if self.user_type == 'pescador':
            new_fish = Fish(type=type, fishDate=fishDate, quantity=quantity, price=price)
            fish = self.search_fish(type)
            if fish is not None:
                fish.add_quantity(quantity)
            else:
                self.fishInventory.append(new_fish)
                db.session.add(new_fish)
                db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
       
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
    
    def add_quantity(self, value):
        if self.quantity > -value:
            self.quantity += value
            db.session.commit()


