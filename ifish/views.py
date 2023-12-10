from flask import Blueprint, render_template, request, flash, jsonify
import json

views = Blueprint('views', __name__)

class ViewsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Views(metaclass=ViewsMeta):
    def showHome(self, current_user, user_fish_inventory):
        user_fish_inventory = current_user.fishInventory  # Get the relationship object
        return render_template("pescador.html", user=current_user, fishes = user_fish_inventory)

    def showStock(self, current_user):
        user_fish_inventory = current_user.fishInventory  # Get the relationship object
        return render_template("estoque.html", user=current_user, fishes = user_fish_inventory)

    def showLogin(self):
        return render_template("login.html")

    def showsignUp(self):
        return render_template("signUp.html")

    def showInitial(self):
        return render_template("init.html")

    def showHomeComprador(self, current_user):
        return render_template("homeComprador.html", user=current_user)

    def showCarrinho(self, current_user, cart):
        return render_template("carrinho.html", user = current_user, transactions = cart.get_transactions() if cart is not None else None)

    def showHistoricoCompras(self, current_user):
        return render_template("historicoCompras.html", transactions = current_user.get_past_transactions())

    def showBuscaComprador(self, fishes):
        return render_template("buscaComprador.html", fishes=fishes)

    def showHomePescador(self, current_user):
        user_fish_inventory = current_user.fishInventory  # Get the relationship object
        return render_template("homePescador.html", user=current_user, fishes = user_fish_inventory, transactions = current_user.get_past_sell())

    def showPerfilComprador(self, user):
        return render_template("perfilComprador.html", user=user)

    def showPerfilPescador(self, user):
        return render_template("perfilPescador.html", user=user)

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
