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
    transactionHistory = db.relationship('Transaction', backref='owner', lazy=True)
    lastTransactionFinished = True

    def __init__(self, name, email, password, userType):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = userType

    def search_own_fish(self, fish_type):
        if fish_type in [i.type for i in self.fishInventory]:
            return Fish.query.filter_by(type=fish_type).filter_by(user_id=self.id).first()
        return None
            
    def add_fish(self, type, fishDate, quantity, price):
        if self.user_type == 'pescador':
            new_fish = Fish(type=type, fishDate=fishDate, quantity=quantity, price=price, transaction_id= 0)
            fish = self.search_own_fish(type)
            if fish is not None:
                fish.add_quantity(quantity)
            else:
                self.fishInventory.append(new_fish)
                db.session.add(new_fish)
                db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
    
    def remove_fish(self, type):
        if self.user_type == 'pescador':
            fish_to_delete = self.search_own_fish(type)
            if fish_to_delete is not None:
                db.session.delete(fish_to_delete)  # Mark the fish object for deletion
                db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
        
    def search_fish_buy(self, fish_type):
        return Fish.query.filter_by(type=fish_type)
    
    def add_transaction(self):
        if self.lastTransactionFinished:
            self.lastTransactionFinished = False
            new_transaction = Transaction()
            self.transactionHistory.append(new_transaction)
            return self.transactionHistory[-1]
        else:
            return self.transactionHistory[-1]
        
    def commit_last_transaction(self):

        if not self.lastTransactionFinished:
            db.session.add(self.transactionHistory[-1])
            db.session.commit()
            self.lastTransactionFinished = True
            self.transactionHistory[-1].commit_transaction()
       
class Fish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    fishDate = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    transaction_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, type, fishDate, quantity, price, transaction_id):
        self.type = type
        self.fishDate = fishDate
        self.quantity = quantity
        self.price = price
        self.transaction_id = transaction_id
    
    def add_quantity(self, value):
        if self.quantity > -value:
            self.quantity += value
            db.session.commit()

    def get_fish_owner(self):
        return User.query.filter_by(id=self.user_id).first()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fisher_id = db.Column(db.Integer)
    temporaryInventory = []
    
    def __init__(self):
        self.cost = 0
    
    def add_fish(self, fish_id, quantity):
        fish = Fish.query.filter_by(id=fish_id).first()
        self.temporaryInventory.append([fish, quantity])
        self.cost += (fish.price * quantity)
        print(self.cost)
    
    def commit_transaction(self):
        for i in self.temporaryInventory:
            new_fish = Fish(type = i[0].type, fishDate = i[0].fishDate, quantity = i[1], price= i[0].price, transaction_id = self.id)
            i[0].add_quantity(-1*i[1])
            
            db.session.add(new_fish)
            db.session.commit()
        del self.temporaryInventory
            


