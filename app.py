from flask import Flask,render_template,flash,request,redirect,url_for,abort
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
from flasker.forms import UserForm,LoginForm,PostForm,PwdForm,NamerForm,SearchForm
from flask_ckeditor import CKEditor
from functools import wraps

from flasker.regressors.dt import train_dt_predictor
from flasker.regressors.predictor import Prediction, Predictor
from flasker.clustering.kmeanscluster import initiate_kmc_predictor
@dataclass
class AppEnvironment:
    api_key: str

# initialiser la bd
db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            abort(403)   # or another page like login or an error page
        return f(*args, **kwargs)
    return decorated_function

from flasker.models import Posts,Users,Articles
from flasker.routes import user_bp,post_bp,test_bp,core_bp,admin_bp,api_bp

def create_app(env: AppEnvironment = None) -> Flask:
    if env is None:
        api_key = os.getenv("API_KEY", "default_api_key")
        env = AppEnvironment(api_key=api_key)

    # créer une instance
    app=Flask(__name__)
    ckeditor=CKEditor(app)
    # ajouter la bd SQLite
    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # ajouter la bd MySQL
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('SQLALCHEMY_DATABASE_URI')#mysql+pymysql://root:Fqm123!@localhost/users'#
    app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER']= os.getenv('UPLOAD_FOLDER', 'static/images/')
    app.config['NAME']= os.getenv('NAME')
    app.config['TITLE']= os.getenv('TITLE')
    app.config['DESCRIPTION']= os.getenv('DESCRIPTION')
    app.config['SITEPHP']= os.getenv('SITEPHP','http://localhost:8000/')
    app.config['BDQM']= os.getenv('BDQM')
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    #db=SQLAlchemy(app)
    #migrate=Migrate(app,db)
    app.dt_predictor=train_dt_predictor(app)
    app.kmc_predictor=initiate_kmc_predictor(app)

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
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def base():
        form=SearchForm()
        return dict(form=form)
    
    return app