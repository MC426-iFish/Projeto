from . import db
from flask_login import UserMixin
from sqlalchemy import Boolean
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    fishInventory = db.relationship('Fish', backref='owner', lazy=True)
    cartInventory = db.relationship('Cart', backref='owner', lazy=True)
    lastTransactionFinished = db.Column(Boolean, default = True)

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
            fish = self.search_own_fish(type)
            if fish is not None:
                fish.add_quantity(quantity)
            else:
                new_fish = Fish(type=type, fishDate=fishDate, quantity=quantity, price=price)
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
    
    def add_cart(self):
        new_cart = Cart()
        self.cartInventory.append(new_cart)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    def add_transaction_fish(self, fish_id, weight):
        if self.lastTransactionFinished:
            #add cart
            new_cart = self.add_cart()
            #add fish to cart
            new_cart.add_transaction(fish_id, weight)
            self.lastTransactionFinished = False
        else:
            cart = Cart.query.filter_by(buyer_id=self.user_id).filter_by(paid = False).first()
            cart.add_transaction(fish_id, weight)
   
    def commit_last_transaction(self):
        if not self.lastTransactionFinished:
            cart = Cart.query.filter_by(buyer_id=self.user_id).filter_by(paid = False).first()
            cart.pay_transactions()
            self.lastTransactionFinished = True
       
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

    def get_fish_owner(self):
        return User.query.filter_by(id=self.user_id).first()

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fisher_id = db.Column(db.Integer)
    paid = db.Column(db.Boolean, default = False)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

    def __init__(self):
        super().__init_()

    def add_transaction(self, fish_id, weight):

        new_transaction = Transaction(fish_id=fish_id, weight=weight)
        self.transactions.append(new_transaction)
        db.session.add(new_transaction)
        db.session.commit()   
        self.cost += new_transaction.compute_cost()

    def pay_transactions(self):
        for i in Transaction.query.filter(cart_id = id):
            i.commit_transaction()
        self.paid = True


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fish_id = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __init__(self, fish_id, weight):
        self.fish_id = fish_id
        self.weight = weight
    
    def compute_cost(self):
        return Fish.query.filter_by(id = self.fish_id).first().price * self.weight
    
    def commit_transaction(self):
        fish = Fish.query.filter_by(id = self.fish_id).first()
        fish.add_quantity(-1*self.weight)
        new_fish = Fish(type=fish.type, fishDate=fish.fishDate, quantity=self.weight, price=fish.price)
        new_fish.user_id = 0
        db.session.add(new_fish)
        db.session.commit()    
            
            


