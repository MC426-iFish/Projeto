from flask import render_template

class ViewsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Views(metaclass=ViewsMeta):

    def showStock(self, current_user):
        user_fish_inventory = current_user.fishInventory  # Get the relationship object9
        return render_template("estoque.html", user=current_user, fishes = current_user.get_fishes())

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
        return render_template("historicoCompras.html", user = current_user, transactions = current_user.get_past_transactions())

    def showBuscaComprador(self, fishes, current_user):
        return render_template("buscaComprador.html", user = current_user, fishes=fishes)

    def showHomePescador(self, current_user):
        totalsum = 0
        user_fish_inventory = current_user.fishInventory  # Get the relationship object

        for i in current_user.get_past_sell():
            totalsum += i.compute_cost()
        return render_template("homePescador.html", user=current_user, fishes = current_user.get_fishes(), transactions = current_user.get_past_sell(), totalsum = totalsum)

    def showPerfilComprador(self, user):
        return render_template("perfilComprador.html", user=user)

    def showPerfilPescador(self, user):
        return render_template("perfilPescador.html", user=user)
