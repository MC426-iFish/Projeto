from flask import Blueprint, request, redirect, url_for
from flask_login import current_user
from .__init__ import getView

pescador = Blueprint('pescador', __name__)
view = getView()

@pescador.route('/homePescador', methods=['GET', 'POST'])
def homePescador():
    if request.method == "POST":
        if request.form['redirect'] == 'Acessar':
            return redirect(url_for("pescador.estoque"))
        if request.form['redirect'] == 'perfil':
            return redirect(url_for("pescador.perfilPescador"))
        if request.form['redirect'] == 'avaliacoes':
            return redirect(url_for("pescador.avaliacoes"))
        
    return view.showHomePescador(current_user)

@pescador.route('/estoque', methods=['GET', 'POST'])
def estoque():
    if request.method == 'POST' and request.form.get('estoqueSubmit') == 'Adicionar':
        tipo = request.form.get('tipoPeixe')
        qtd = request.form.get('quantidadePeixe')
        preco = request.form.get('precoPeixe')
        current_user.add_fish(tipo, '2023-10-23', int(qtd), int(preco))
        qtd = 0
    elif request.method == 'POST' and request.form.get('removersubmit') == 'Remover':
        fish_type_price = request.form.get('OPCAO').replace("'", "").strip("''()").split(', ')
        current_user.remove_fish(fish_type_price[0], fish_type_price[1])
    elif request.method == 'POST' and request.form.get('redirect') == 'home':
        return redirect(url_for("pescador.homePescador"))

    return view.showStock(current_user)

@pescador.route('/perfilPescador', methods=['GET', 'POST'])
def perfilPescador():
    user = current_user
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for("pescador.homePescador"))
        elif request.form['redirect'] == 'Logout':
            return redirect(url_for("auth.logout"))
        elif request.form['redirect'] == 'Mais Detalhes':
            return redirect(url_for("pescador.avaliacoes"))
        elif request.form['redirect'] == 'Alterar Senha':
            return redirect(url_for("alterador.alterarSenha"))
        elif request.form['redirect'] == 'Trocar':
            return redirect(url_for("alterador.alterarUser"))
        
    return view.showPerfilPescador(user)

@pescador.route('/avaliacoes', methods=['GET', 'POST'])
def avaliacoes():
    user = current_user
    if request.method == "POST":
        if request.form['redirect'] == 'home':
            return redirect(url_for("pescador.homePescador"))    
    return view.showAvaliacoes(user)
