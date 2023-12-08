from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from .views import showHomePescador, showStock
from flask_login import current_user


pescador = Blueprint('pescador', __name__)

@pescador.route('/homePescador', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.form['acessStock'] == 'Acessar':
            return redirect(url_for("auth.estoque"))
        
    return showHomePescador()

@pescador.route('/estoque', methods=['GET', 'POST'])
def estoque():
    if request.method == 'POST' and request.form.get('estoqueSubmit') == 'Adicionar':
        tipo = request.form.get('tipoPeixe')
        qtd = request.form.get('quantidadePeixe')
        preco = request.form.get('precoPeixe')
        current_user.add_fish(tipo, '2023-10-23', int(qtd), int(preco))
        qtd = 0

    if request.method == 'POST' and request.form.get('removersubmit') == 'Remover':
        fish_type = request.form.get('OPCAO')
        current_user.remove_fish(fish_type)

    return showStock()