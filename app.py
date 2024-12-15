from flask import Flask,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from flask_migrate import Migrate
import os
from datetime import date
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import LoginManager,login_required,UserMixin,logout_user,current_user,login_user
from flasker.forms import UserForm,LoginForm,PostForm,PwdForm,NamerForm


@dataclass
class AppEnvironment:
    api_key: str

# initialiser la bd
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()

from flasker.models import Posts,Users
from flasker.routes import user_bp,post_bp,test_bp,core_bp

def create_app(env: AppEnvironment = None) -> Flask:
    if env is None:
        api_key = os.getenv("API_KEY", "default_api_key")
        env = AppEnvironment(api_key=api_key)

    # créer une instance
    app=Flask(__name__)

    # ajouter la bd SQLite
    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # ajouter la bd MySQL
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI')#mysql+pymysql://root:Fqm123!@localhost/users'#
    app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    #db=SQLAlchemy(app)
    #migrate=Migrate(app,db)

    @app.route('/date')
    def get_curr_date():
        fav={
            "John":"kk",
            "Maria":"funny"
        }
        return {"Date":date.today(),
                "Fav":fav} # dic = json en Python

    # Flask login
    login_manager.init_app(app)
    login_manager.login_view='core_bp.login'
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(test_bp)
    app.register_blueprint(core_bp)

    

    return app