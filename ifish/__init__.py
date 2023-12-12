from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import Views

db = SQLAlchemy()
DB_NAME = "MC426.db"

view = Views()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MC426ifish'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .authController import auth
    from .compradorController import comprador
    from .pescadorController import pescador

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(comprador, url_prefix='/')
    app.register_blueprint(pescador, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)

def getView():
    return view
