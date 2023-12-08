from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from .utils import signup_validator
from .views import showLogin, showsignUp, showInitial, showStock


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def initial():
    if request.method == "POST":
        if request.form['redirect'] == 'Fazer Login':
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.sign_up'))
        
    return showInitial()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and 'loginEmail' in request.form:
        userEmail = request.form["loginEmail"]
        userPassword = request.form["loginPassword"]
        userType = request.form.get('OPCAO')

        if userType == 'comprador':
            user = User.query.filter_by(email=userEmail).first()
            print("this is type:", type(user))
            user=user if user.user_type == 'comprador' else None
        else:
            user = User.query.filter_by(email=userEmail).first()
            print("this is type:", type(user))
            user=user if user.user_type == 'pescador' else None

        if not user:
            flash('Usuario não existe', category='error')
            
        elif(userPassword == user.password):      

            login_user(user, remember=True)

            if userType == 'comprador':
                return redirect(url_for("comprador.homeComprador"))
            elif userType == 'pescador':
                return redirect(url_for("pescador.homePescador"))

        else:
            flash('Senha incorreta', category='error')
            
    

    return showLogin()


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
            newUser = User(name=name, email=email, password=password, userType=userType)
        
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)                    
            flash('Conta Criada com Sucesso!', category='sucess')

            if newUser.user_type == 'comprador':
                return redirect(url_for("comprador.homeComprador"))
            elif newUser.user_type == 'pescador':
                return redirect(url_for("pescador.homePescador"))
        
    return showsignUp()



