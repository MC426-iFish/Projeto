from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from utils import signup_validator


app = Flask(__name__)
app.secret_key = "MC426ifish"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["loginEmail"]
        userPassword = request.form["loginPassword"]
        session["userEmail"] = userEmail
        if(User.query.filter_by(email=userEmail).first() == None):
            
            flash('Usuario não existe', category='danger')
            
        elif(userPassword == User.query.filter_by(email=userEmail).first().password):
            return redirect(url_for("user"))
        else:
            flash('Senha incorreta', category='danger')
            
    
    return render_template("login.html")

@app.route("/signUp", methods=["GET", "POST"])
def signUpForm():
    if request.method == "POST":
        name = request.form.get('fullName')
        email = request.form.get('singUpEmail')
        password = request.form.get('signUpPassword')
        passwordCheck = request.form.get('signUpPasswordCheck')
        user = User.query.filter_by(email=email).first()
        message, validation = signup_validator.validate(name, email, password, passwordCheck, user)
        if not validation:
            flash(message, category='danger')    
        else:
            newUser = User(name=name, email=email, password=password)
            db.session.add(newUser)
            db.session.commit()
            Email = request.form["singUpEmail"]                           
            session["userEmail"] = Email                                  
            flash('Conta Criada com Sucesso!', category='sucess')
            return redirect(url_for("user"))
        
    return render_template("signUp.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("userEmail", None)
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "userEmail" in session:
        userEmail = session["userEmail"]
        return render_template("user.html", userEmail=userEmail)
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True)

