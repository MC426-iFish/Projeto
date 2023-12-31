from . import db
from flask_login import UserMixin
from sqlalchemy import Boolean

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    fishInventory = db.relationship('Fish', backref='owner', lazy=True)
    cartInventory = db.relationship('Cart', backref='owner', lazy=True)
    lastTransactionFinished = db.Column(Boolean, default = True)
    evaluations = db.relationship("Evaluation", backref='owner', lazy=True)

    def __init__(self, name, email, password, userType):
        self.name = name
        self.email = email
        self.password = password
        self.user_type = userType

    def search_own_fish(self, fish_type, price):
        if fish_type in [i.type for i in self.fishInventory]:
            return Fish.query.filter_by(type=fish_type).filter_by(user_id=self.id).filter_by(price = price).first()
        return None
            
    def add_fish(self, type, fishDate, quantity, price):
        if self.user_type == 'pescador':
            fish = self.search_own_fish(type, price)
            if fish is not None:
                fish.add_quantity(quantity)
            else:
                new_fish = Fish(type=type, fishDate=fishDate, quantity=quantity, price=price)
                self.fishInventory.append(new_fish)
                db.session.add(new_fish)
                db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
    
    def add_evaluation(self, comment, grade, comentor):
        if self.user_type == 'pescador':
            new_evaluation = Evaluation(comment=comment, grade=grade, comentor_id = comentor.id)
            self.evaluations.append(new_evaluation)
            db.session.add(new_evaluation)
            db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
        
    def get_evaluation_grade(self):
        if self.user_type == 'pescador':
            grade = 0
            count = 0
            for evaluation in self.evaluations:
                grade += evaluation.grade
                count += 1
            if count != 0:
                grade = grade / count
                return grade
            return 5
        else:
            raise PermissionError("Shouldn't be allowed")

    def remove_fish(self, type, price):
        if self.user_type == 'pescador':
            fish_to_delete = self.search_own_fish(type, price)
            if fish_to_delete is not None:
                db.session.delete(fish_to_delete)  # Mark the fish object for deletion
                db.session.commit()
        else:
            raise PermissionError("Shouldn't be allowed")
        
    def search_fish_buy(self, fish_type):
        return [i for i in Fish.query.filter_by(type=fish_type).all() if (i.user_id != 0 and i.quantity > 0)]
    
    def add_cart(self):
        new_cart = Cart()
        self.cartInventory.append(new_cart)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    def add_transaction_fish(self, fish_id, weight):
        if Fish.query.filter_by(id = fish_id).first().quantity >= weight:
            if self.lastTransactionFinished:
                new_cart = self.add_cart() #add cart
                new_cart.add_transaction(fish_id, weight, Fish.query.filter_by(id = fish_id).first().user_id) #add fish to cart
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
            db.session.commit()
        
    def get_active_transaction(self):
        if not self.lastTransactionFinished:
            return Cart.query.filter_by(buyer_id=self.id).filter_by(paid = False).first()
        return None   
    
    def get_past_transactions(self):
        past_transactions = []
        for i in Cart.query.filter_by(buyer_id = self.id).order_by(Cart.id.desc()).all():
            if i.paid:
                past_transactions.extend(Transaction.query.filter_by(cart_id = i.id).all())
        return past_transactions
    
    def get_past_sell(self):
        past_transactions = []
        for i in Transaction.query.filter_by(fisher_id = self.id).order_by(Transaction.id.desc()).all():
            if Cart.query.filter_by(id = i.cart_id).first().paid:
                past_transactions.append(i)
        return past_transactions
     
    def get_fishes(self):
        return Fish.query.filter(Fish.user_id == self.id, Fish.quantity > 0).all()
    
    def get_evaluations(self):
        return self.evaluations
    
    def get_last_fisher(self):
        last_transaction = None
        last_cart = Cart.query.filter_by(buyer_id = self.id).order_by(Cart.id.desc()).first()
        if last_cart.paid:
            last_transaction = Transaction.query.filter_by(cart_id = last_cart.id).first()
            return last_transaction.get_fisher()
        return last_transaction
    
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
        if self.quantity >= -value:
            self.quantity += value
            db.session.commit()

    def get_fish_owner(self):
        return User.query.filter_by(id=self.user_id).first()
    
class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200))
    grade = db.Column(db.Integer)
    comentor_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, comment, grade, comentor_id):
        self.comment = comment
        self.grade = grade
        self.comentor_id = comentor_id
    
    def get_evaluation_owner(self):
        return User.query.filter_by(id=self.user_id).first()
    
    def get_evaluator_name(self):
        return User.query.filter_by(id=self.comentor_id).first().name

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Integer)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    paid = db.Column(db.Boolean, default = False)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

    def __init__(self):
        self.cost = 0

    def add_transaction(self, fish_id, weight, fisher_id):
        
        #filter if there already is a transaction for same fish_id
        previous = Transaction.query.filter(Transaction.cart_id == self.id).filter(Transaction.fish_id == fish_id).first()

        if previous is not None:
            previous.add_quantity(weight)
        else:

            new_transaction = Transaction(fish_id=fish_id, weight=weight, fisher_id = fisher_id)
            self.transactions.append(new_transaction)
            db.session.add(new_transaction)
            db.session.commit()   
            self.cost += new_transaction.compute_cost()
            db.session.commit()   

    def pay_transactions(self):
        for i in Transaction.query.filter(Transaction.cart_id == self.id).all():
            
            if not i.can_commit():
                db.session.delete(i)
                print("Não foi possível concluir a compra")

        for i in Transaction.query.filter(Transaction.cart_id == self.id).all():
            print("Commiting transaction", i.id)
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
    
    def can_commit(self):
        fish = Fish.query.filter_by(id = self.fish_id).first()
        if(fish.quantity >= self.weight):
            return True
        return False   

    def commit_transaction(self):
        fish = Fish.query.filter_by(id = self.fish_id).first()
        if(fish.quantity >= self.weight):
            fish = Fish.query.filter_by(id = self.fish_id).first()
            fish.add_quantity(-1*self.weight)
            new_fish = Fish(type=fish.type, fishDate=fish.fishDate, quantity=self.weight, price=fish.price)
            new_fish.user_id = 0
            db.session.add(new_fish)
            if fish.quantity == 0:
                db.session.commit()
                self.fish_id = new_fish.id 
            
            db.session.commit()
             

    def get_fish_type(self):
        return Fish.query.filter_by(id = self.fish_id).first().type

    def get_fisher_name(self):
        return User.query.filter_by(id = self.fisher_id).first().name
    
    def get_fisher(self):
        return User.query.filter_by(id = self.fisher_id).first()
    
    def get_fisher_grade(self):
        return User.query.filter_by(id = self.fisher_id).first().get_evaluation_grade()
    
    def get_buyer_name(self):
        buyer_id = Cart.query.filter_by(id = self.cart_id).first().buyer_id
        return User.query.filter_by(id = buyer_id).first().name

    def add_quantity(self, int):
        self.weight += int
        db.session.commit()