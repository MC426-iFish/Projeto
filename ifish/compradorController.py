from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db   
from .utils import signup_validator
from .views import showHomeComprador, showCarrinho, showHistoricoCompras, showBuscaComprador


comprador = Blueprint('comprador', __name__)


@comprador.route('/homeComprador', methods=['GET', 'POST'])
def homeComprador():        
    return showHomeComprador()

@comprador.route('/carrinho', methods=['GET', 'POST'])
def carrinho():        
    return showCarrinho()

@comprador.route('/historicoCompras', methods=['GET', 'POST'])
def historicoCompras():        
    return showHistoricoCompras()

@comprador.route('/buscaComprador', methods=['GET', 'POST'])
def buscaComprador():        
    return showBuscaComprador()
