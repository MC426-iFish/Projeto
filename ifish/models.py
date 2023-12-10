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
            new_cart.add_transaction(fish_id, weight, Fish.query.filter_by(id = fish_id).first().user_id)
            self.lastTransactionFinished = False
            db.session.commit()
        else:
            cart = Cart.query.filter_by(buyer_id=self.id).filter_by(paid = False).first()
            cart.add_transaction(fish_id, weight, Fish.query.filter_by(id = fish_id).first().user_id)
            db.session.commit()
   
    def commit_last_transaction(self):
        if not self.lastTransactionFinished:
            cart = Cart.query.filter_by(buyer_id=self.id).filter_by(paid = False).first()
            cart.pay_transactions()
            self.lastTransactionFinished = True
        
    def get_active_transaction(self):
        if not self.lastTransactionFinished:
            return Cart.query.filter_by(buyer_id=self.id).filter_by(paid = False).first()
        return None   
    
    def get_past_transactions(self):
        past_transactions = []
        for i in Cart.query.filter_by(buyer_id = self.id).all():
            past_transactions.extend(Transaction.query.filter_by(cart_id = i.id).all())
        return past_transactions
    
    def get_past_sell(self):
        
        return Transaction.query.filter_by(fisher_id = self.id).all()
    
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
    paid = db.Column(db.Boolean, default = False)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

    def __init__(self):
        self.cost = 0

    def add_transaction(self, fish_id, weight, fisher_id):

        new_transaction = Transaction(fish_id=fish_id, weight=weight, fisher_id = fisher_id)
        self.transactions.append(new_transaction)
        db.session.add(new_transaction)
        db.session.commit()   
        self.cost += new_transaction.compute_cost()
        db.session.commit()   

    def pay_transactions(self):
        for i in Transaction.query.filter(Transaction.cart_id == self.id).all():
            i.commit_transaction()
        self.paid = True
        db.session.commit()   

    def get_transactions(self):
        return Transaction.query.filter(Transaction.cart_id == self.id).all()
    

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fish_id = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    fisher_id  = db.Column(db.Integer)

    def __init__(self, fish_id, weight, fisher_id):
        self.fish_id = fish_id
        self.weight = weight
        self.fisher_id = fisher_id
    
    def compute_cost(self):
        return (Fish.query.filter_by(id = self.fish_id).first().price) * (self.weight)
    
    def commit_transaction(self):
        fish = Fish.query.filter_by(id = self.fish_id).first()
        fish.add_quantity(-1*self.weight)
        new_fish = Fish(type=fish.type, fishDate=fish.fishDate, quantity=self.weight, price=fish.price)
        new_fish.user_id = 0
        db.session.add(new_fish)
        db.session.commit()    

    def get_fish_type(self):
        return Fish.query.filter_by(id = self.fish_id).first().type

    def get_fisher_name(self):
        return User.query.filter_by(id = self.fisher_id).first().name
    
    def get_buyer_name(self):
        return User.query.filter_by(id = Cart.query.filter_by(id = self.cart_id).first().buyer_id).first().name
            
            


