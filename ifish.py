from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

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

@app.route("/user")
def user():
    if "userEmail" in session:
        userEmail = session["userEmail"]
        return f"<h1>{userEmail}</h1>"
    else:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)