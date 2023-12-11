# from ifish import *
# from .utils import *

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = "MC426.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MC426ifish'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER']= "smtp.gmail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = "enzo_man@gmail.com"
    app.config['MAIL_PASSWORD'] = "adsfxcv43"
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .alteradorController import alterador

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(alterador, url_prefix='/')

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

def create_email(app):
    return Mail(app)

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
