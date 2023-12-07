from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from .utils import signup_validator
from .views import showHomeComprador, showCarrinho, showHistoricoCompras, showBuscaComprador


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
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for('comprador.homeComprador'))
             
    return showBuscaComprador()
