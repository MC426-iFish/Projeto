from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form['alterar'] == 'alterar Senha':
            return redirect(url_for('alterador.alterarSenha'))
        else:
            return redirect(url_for('alterador.alterarUser'))
    return render_template("user.html", user=current_user)

def showLogin():
    return render_template("login.html")

def showsignUp():
    return render_template("signUp.html")

def showInitial():
    return render_template("init.html")

def showAlterarUser():
    return render_template("alterarUser.html")

def showAlterarSenha():
    return render_template("alterarSenha.html")

# @views.route()
# def showHome():
#     return render_template("user.html")

# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
