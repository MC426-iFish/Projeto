from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from .views import showAlterarSenha, showAlterarUser

alterador = Blueprint('alterador', __name__)

@alterador.route('/alterarUser', methods=["GET", "POST"])
@login_required
def alterarUser():   
    return showAlterarUser()

@alterador.route('/alterarSenha', methods=["GET", "POST"])
@login_required
def alterarSenha():
    return showAlterarSenha()