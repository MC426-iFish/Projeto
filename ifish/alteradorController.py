from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message 
from .views import showAlterarSenha, showAlterarUser
from .emailController import enviar

alterador = Blueprint('alterador', __name__)


@alterador.route('/alterarUser', methods=["GET", "POST"])
@login_required
def alterarUser():
    if request.method == "POST":
        userName = request.form.get('Usuario')
        current_user.name = userName
        db.session.commit()
        return redirect(url_for("views.home"))
    return showAlterarUser()    

@alterador.route('/alterarSenha', methods=["GET", "POST"])
@login_required
def alterarSenha():
    if request.method == "POST":
     userCurr = request.form.get("senha-atual")
     userNew = request.form.get("nova-senha")
     if userNew == request.form.get("confirmar-senha"):
         current_user.password = userNew
         db.session.commit()
         return redirect(url_for("views.home"))
    return showAlterarSenha()