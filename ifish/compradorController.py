from flask import Blueprint, request, redirect, url_for
from flask_login import current_user
from .__init__ import getView

comprador = Blueprint('comprador', __name__)
view = getView()

@comprador.route('/homeComprador', methods=['GET', 'POST'])
def homeComprador():      
    if request.method == "POST":
        if request.form['redirect'] == 'carrinho':
            return redirect(url_for('comprador.carrinho'))
        elif request.form['redirect'] == 'historico':
            return redirect(url_for('comprador.historicoCompras'))
        elif request.form['redirect'] == 'busca':
            return redirect(url_for('comprador.buscaComprador'))
        elif request.form['redirect'] == 'perfil':
            return redirect(url_for('comprador.perfilComprador'))

    return view.showHomeComprador(current_user)

@comprador.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if request.method == "POST":
        if request.form.get('redirect') == 'home':
            return redirect(url_for('comprador.homeComprador'))
        elif request.form.get('continuar') == 'Continuar':
            current_user.commit_last_transaction()

    return view.showCarrinho(current_user, cart = current_user.get_active_transaction())

@comprador.route('/historicoCompras', methods=['GET', 'POST'])
def historicoCompras():
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))

    return view.showHistoricoCompras(current_user)

@comprador.route('/buscaComprador', methods=['GET', 'POST'])
def buscaComprador():
    fishes = None
    if request.method == "POST" and 'redirect' in request.form:
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))
    elif request.method == "POST" and 'busca' in request.form:
        fish_type = request.form.get('busca')
        fishes = current_user.search_fish_buy(fish_type)
    elif request.method == "POST" and request.form.get('compraSubmit') == 'Adicionar':
        chosen_fish = request.form.get('OPCAO')
        peso = request.form.get('pesoPeixe')
        current_user.add_transaction_fish(chosen_fish, int(peso)) 

    return view.showBuscaComprador(fishes)

@comprador.route('/perfilComprador', methods=['GET', 'POST'])
def perfilComprador():   
    user = current_user     
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))

    return view.showPerfilComprador(user)
