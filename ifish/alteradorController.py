from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from .views import showAlterarSenha, showAlterarUser

alterador = Blueprint('alterador', __name__)

@alterador.route('/alterarUser', methods=["GET", "POST"])
@login_required
def alterarUser():
    userName = request.form.get('Usuario')
    current_user.name = userName
    db.session.commit()
    return showAlterarUser()

@alterador.route('/alterarSenha', methods=["GET", "POST"])
@login_required
def alterarSenha():
    userCurr = request.form.get("senha-atual")
    userNew = request.form.get("nova-senha")
    if userNew == request.form.get("confirmar-senha"):
        current_user.password = userNew
        db.session.commit()
        return showAlterarSenha()