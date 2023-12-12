from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message 
from .views import showAlterarSenha, showAlterarUser
import smtplib, ssl

alterador = Blueprint('alterador', __name__)

@alterador.route('/alterarUser', methods=["GET", "POST"])
@login_required
def alterarUser():
    if request.method == "POST":
        userName = request.form.get('Usuario')
        current_user.name = userName
        db.session.commit()
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "enzofarias656@gmail.com"  # Enter your address
        receiver_email = current_user.email  # Enter receiver address
        password = "adsfxcv43"
        message = """\
          Subject: Hi there

        This message is sent from Python."""
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
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
         port = 465  # For SSL
         smtp_server = "smtp.gmail.com"
         sender_email = "enzofarias656@gmail.com"  # Enter your address
         receiver_email = current_user.email  # Enter receiver address
         password = "adsfxcv43"
         message = """\
          Subject: Hi there

        This message is sent from Python."""
         context = ssl.create_default_context()
         with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
         return redirect(url_for("views.home"))
     elif userNew != request.form.get("confirmar-senha"):
        flash('Senhas não compativeis', category='error')
     else:
        flash('Senha atual invalida', category = 'error')
    return showAlterarSenha()