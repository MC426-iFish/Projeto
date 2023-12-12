from flask import Blueprint, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user
from .utils import signup_validator
from .__init__ import getView

auth = Blueprint('auth', __name__)
view = getView()

@auth.route('/', methods=['GET', 'POST'])
def initial():
    if request.method == "POST":
        if request.form['redirect'] == 'Fazer Login':
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.sign_up'))

    return view.showInitial()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and 'loginEmail' in request.form:
        userEmail = request.form["loginEmail"]
        userPassword = request.form["loginPassword"]
        userType = request.form.get('OPCAO')
        user = User.query.filter_by(email=userEmail).first()
        if checkUserExists(user):
            if checkCorrectUserType(user, userType):
                return loginAuth(user, userPassword)
    elif request.method == "POST" and request.form["loginSubmit"] == "Criar conta":
        return redirect(url_for("auth.sign_up"))
            
    return view.showLogin()

def checkUserExists(user):
    if not user:
        flash('Usuario não existe', category='error')
        return False
    return True

def checkCorrectUserType(user, userType):
    if user.user_type != userType:
        flash('Tipo de usuário incorreto', category='error')
        return False
    return True

def loginAuth(user, userPassword):
    if(userPassword == user.password):
        login_user(user, remember=True)
        if user.user_type == "comprador":
            return redirect(url_for("comprador.homeComprador"))
        else:
            return redirect(url_for("pescador.homePescador"))
    else:
        flash('Senha incorreta', category='error')
        return view.showLogin()

@auth.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signUp', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST" and 'singUpEmail' in request.form:
        name = request.form.get('fullName')
        email = request.form.get('singUpEmail')
        password = request.form.get('signUpPassword')
        passwordCheck = request.form.get('signUpPasswordCheck')
        userType = request.form.get('OPCAO')
        user = User.query.filter_by(email=email).first()
        message, validation = signup_validator.validate(name, email, password, passwordCheck, user)
        if not validation:
            flash(message, category='error')    
        else:
            return createAndLoginUser(name, email, password, userType)
    elif request.method == "POST" and request.form.get('singUpSubmit') == "Fazer login":
        return redirect(url_for("auth.login"))
        
    return view.showsignUp()

def createAndLoginUser(name, email, password, userType):
    newUser = User(name=name, email=email, password=password, userType=userType)
    db.session.add(newUser)
    db.session.commit()
    login_user(newUser, remember=True)                    
    if newUser.user_type == 'comprador':
        return redirect(url_for("comprador.homeComprador"))
    elif newUser.user_type == 'pescador':
        return redirect(url_for("pescador.homePescador"))
