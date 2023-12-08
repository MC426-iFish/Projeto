from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db   
from .utils import signup_validator
from .views import showHomeComprador, showCarrinho, showHistoricoCompras, showBuscaComprador
from flask_login import current_user


comprador = Blueprint('comprador', __name__)


@comprador.route('/homeComprador', methods=['GET', 'POST'])
def homeComprador():      
    if request.method == "POST":
        if request.form['redirect'] == 'carrinho':
            return redirect(url_for('comprador.carrinho'))
        elif request.form['redirect'] == 'historico':
            return redirect(url_for('comprador.historicoCompras'))
        elif request.form['redirect'] == 'busca':
            return redirect(url_for('comprador.buscaComprador'))

    return showHomeComprador()

@comprador.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))

    return showCarrinho()

@comprador.route('/historicoCompras', methods=['GET', 'POST'])
def historicoCompras():
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))

    return showHistoricoCompras()

@comprador.route('/buscaComprador', methods=['GET', 'POST'])
def buscaComprador():
    fishes = None
    if request.method == "POST" and 'redirect' in request.form:
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))
    elif request.method == "POST" and 'busca' in request.form:
        fish_type = request.form.get('busca')
        fishes = current_user.search_fish_buy(fish_type)
             
    return showBuscaComprador(fishes)
